import logging
from typing import Optional

from aiosmtpd.controller import Controller
from aiosmtpd.smtp import MISSING, SMTP, syntax

log = logging.getLogger("mail.log")


class PatchedController(Controller):
    def factory(self):
        """Subclasses can override this to customize the handler/server creation."""
        return PatchedSMTP(self.handler, **self.SMTP_kwargs)


class PatchedSMTP(SMTP):
    @syntax("MAIL FROM: <address>", extended=" [SP <mail-parameters>]")
    async def smtp_MAIL(self, arg: Optional[str]) -> None:
        if await self.check_helo_needed():
            return
        if await self.check_auth_needed("MAIL"):
            return
        syntaxerr = "501 Syntax: MAIL FROM: <address>"
        assert self.session is not None
        if self.session.extended_smtp:
            syntaxerr += " [SP <mail-parameters>]"
        if arg is None:
            await self.push(syntaxerr)
            return
        arg = self._strip_command_keyword("FROM:", arg)
        if arg is None:
            await self.push(syntaxerr)
            return
        address, addrparams = self._getaddr(arg)
        if address is None:
            await self.push("553 5.1.3 Error: malformed address")
            return
        if not address:
            await self.push(syntaxerr)
            return
        if not self.session.extended_smtp and addrparams:
            await self.push(syntaxerr)
            return
        assert self.envelope is not None
        if self.envelope.mail_from:
            await self.push("503 Error: nested MAIL command")
            return
        assert addrparams is not None
        mail_options = addrparams.upper().split()
        params = self._getparams(mail_options)
        if params is None:
            await self.push(syntaxerr)
            return
        if not self._decode_data:
            body = params.pop("BODY", "7BIT")
            if body not in ["7BIT", "8BITMIME"]:
                await self.push("501 Error: BODY can only be one of 7BIT, 8BITMIME")
                return
        smtputf8 = params.pop("SMTPUTF8", False)
        if not isinstance(smtputf8, bool):
            await self.push("501 Error: SMTPUTF8 takes no arguments")
            return
        if smtputf8 and not self.enable_SMTPUTF8:
            await self.push("501 Error: SMTPUTF8 disabled")
            return
        self.envelope.smtp_utf8 = smtputf8
        size = params.pop("SIZE", None)
        if size:
            if isinstance(size, bool) or not size.isdigit():
                await self.push(syntaxerr)
                return
            elif self.data_size_limit and int(size) > self.data_size_limit:
                await self.push(
                    "552 Error: message size exceeds fixed maximum message " "size"
                )
                return
        """
        if len(params) > 0:
            await self.push(
                '555 MAIL FROM parameters not recognized or not implemented')
            return
        """
        status = await self._call_handler_hook("MAIL", address, mail_options)
        if status is MISSING:
            self.envelope.mail_from = address
            self.envelope.mail_options.extend(mail_options)
            status = "250 OK"
        log.info("%r sender: %s", self.session.peer, address)
        await self.push(status)

    @syntax("RCPT TO: <address>", extended=" [SP <mail-parameters>]")
    async def smtp_RCPT(self, arg: Optional[str]) -> None:
        if await self.check_helo_needed():
            return
        if await self.check_auth_needed("RCPT"):
            return
        assert self.envelope is not None
        if not self.envelope.mail_from:
            await self.push("503 Error: need MAIL command")
            return

        syntaxerr = "501 Syntax: RCPT TO: <address>"
        assert self.session is not None
        if self.session.extended_smtp:
            syntaxerr += " [SP <mail-parameters>]"
        if arg is None:
            await self.push(syntaxerr)
            return
        arg = self._strip_command_keyword("TO:", arg)
        if arg is None:
            await self.push(syntaxerr)
            return
        address, params = self._getaddr(arg)
        if address is None:
            await self.push("553 5.1.3 Error: malformed address")
            return
        if not address:
            await self.push(syntaxerr)
            return
        if not self.session.extended_smtp and params:
            await self.push(syntaxerr)
            return
        assert params is not None
        rcpt_options = params.upper().split()
        params_dict = self._getparams(rcpt_options)
        if params_dict is None:
            await self.push(syntaxerr)
            return
        # XXX currently there are no options we recognize.
        """
        if len(params_dict) > 0:
            await self.push(
                '555 RCPT TO parameters not recognized or not implemented'
            )
            return
        """
        status = await self._call_handler_hook("RCPT", address, rcpt_options)
        if status is MISSING:
            self.envelope.rcpt_tos.append(address)
            self.envelope.rcpt_options.extend(rcpt_options)
            status = "250 OK"
        log.info("%r recip: %s", self.session.peer, address)
        await self.push(status)
