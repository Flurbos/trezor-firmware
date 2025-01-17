# This file is part of the Trezor project.
#
# Copyright (C) 2012-2019 SatoshiLabs and contributors
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

# XDR decoding tool available at:
#   https://www.stellar.org/laboratory/#xdr-viewer
#
# ## Test Info
#
# The default mnemonic generates the following Stellar keypair at path 44'/148'/0':
#   GAK5MSF74TJW6GLM7NLTL76YZJKM2S4CGP3UH4REJHPHZ4YBZW2GSBPW
#   SDE2YU4V2IYSJIUH7MONDYZTSSLDXV5QDEGUUOLCU4TK7CZWTAXZ5CEG
#
# ### Testing a new Operation
#
# 1. Start at the Stellar transaction builder: https://www.stellar.org/laboratory/#txbuilder?network=test
#   (Verify that the "test" network is active in the upper right)
#
# 2. Fill out the fields at the top as follows:
#   Source account: GAK5MSF74TJW6GLM7NLTL76YZJKM2S4CGP3UH4REJHPHZ4YBZW2GSBPW
#   Transaction sequence number: 4294967296 (see _create_msg)
#   Base fee: 100
#   Memo: None
#   Time Bounds: <leave blank>
#
# 3. Select the operation to test, such as Create Account
#
# 4. Fill out the fields for the operation
#
# 5. Scroll down to the bottom of the page and click "Sign in Transaction Signer"
#
# 6. In the first "Add Signer" text box enter the secret key: SDE2YU4V2IYSJIUH7MONDYZTSSLDXV5QDEGUUOLCU4TK7CZWTAXZ5CEG
#
# 7. Scroll down to the bottom and look at the "signatures" section. The Trezor should generate the same signature
#

from base64 import b64encode

import pytest

from trezorlib import messages as proto, stellar
from trezorlib.tools import parse_path

from .common import MNEMONIC12, TrezorTest


@pytest.mark.altcoin
@pytest.mark.stellar
class TestMsgStellarSignTransaction(TrezorTest):

    ADDRESS_N = parse_path(stellar.DEFAULT_BIP32_PATH)
    NETWORK_PASSPHRASE = "Test SDF Network ; September 2015"

    @pytest.mark.setup_client(mnemonic=MNEMONIC12)
    def test_sign_tx_bump_sequence_op(self, client):
        op = proto.StellarBumpSequenceOp()
        op.bump_to = 0x7FFFFFFFFFFFFFFF
        tx = self._create_msg()

        response = stellar.sign_tx(
            client, tx, [op], self.ADDRESS_N, self.NETWORK_PASSPHRASE
        )
        assert (
            b64encode(response.signature)
            == b"ZMIfHWhpyXdg40PzwOtkcXYnbZIO12Qy0WvkGqoYpb7jyWbG2HQCG7dgWhCoU5K81pvZTA2pMwiPjMwCXA//Bg=="
        )

    @pytest.mark.setup_client(mnemonic=MNEMONIC12)
    def test_sign_tx_account_merge_op(self, client):
        op = proto.StellarAccountMergeOp()
        op.destination_account = (
            "GBOVKZBEM2YYLOCDCUXJ4IMRKHN4LCJAE7WEAEA2KF562XFAGDBOB64V"
        )

        tx = self._create_msg()

        response = stellar.sign_tx(
            client, tx, [op], self.ADDRESS_N, self.NETWORK_PASSPHRASE
        )

        assert (
            response.public_key.hex()
            == "15d648bfe4d36f196cfb5735ffd8ca54cd4b8233f743f22449de7cf301cdb469"
        )
        assert (
            b64encode(response.signature)
            == b"2R3Pj89U+dWrqy7otUrLLjtANjAg0lmBQL8E+89Po0Y94oqZkauP8j3WE7+/z7vF6XvAMLoOdqRYkUzr2oh7Dg=="
        )

    @pytest.mark.setup_client(mnemonic=MNEMONIC12)
    def test_sign_tx_create_account_op(self, client):
        """Create new account with initial balance of 100.0333"""

        op = proto.StellarCreateAccountOp()
        op.new_account = "GBOVKZBEM2YYLOCDCUXJ4IMRKHN4LCJAE7WEAEA2KF562XFAGDBOB64V"
        op.starting_balance = 1000333000

        tx = self._create_msg()

        response = stellar.sign_tx(
            client, tx, [op], self.ADDRESS_N, self.NETWORK_PASSPHRASE
        )

        assert (
            b64encode(response.signature)
            == b"vrRYqkM4b54NrDR05UrW7ZHU7CNcidV0fn+bk9dqOW1bCbmX3YfeRbk2Tf1aea8nr9SD0sfBhtrDpdyxUenjBw=="
        )

    @pytest.mark.setup_client(mnemonic=MNEMONIC12)
    def test_sign_tx_payment_op_native(self, client):
        """Native payment of 50.0111 XLM to GBOVKZBEM2YYLOCDCUXJ4IMRKHN4LCJAE7WEAEA2KF562XFAGDBOB64V"""

        op = proto.StellarPaymentOp()
        op.amount = 500111000
        op.destination_account = (
            "GBOVKZBEM2YYLOCDCUXJ4IMRKHN4LCJAE7WEAEA2KF562XFAGDBOB64V"
        )

        tx = self._create_msg()

        response = stellar.sign_tx(
            client, tx, [op], self.ADDRESS_N, self.NETWORK_PASSPHRASE
        )

        assert (
            b64encode(response.signature)
            == b"pDc6ghKCLNoYbt3h4eBw+533237m0BB0Jp/d/TxJCA83mF3o5Fr4l5vwAWBR62hdTWAP9MhVluY0cd5i54UwDg=="
        )

    @pytest.mark.setup_client(mnemonic=MNEMONIC12)
    def test_sign_tx_payment_op_native_explicit_asset(self, client):
        """Native payment of 50.0111 XLM to GBOVKZBEM2YYLOCDCUXJ4IMRKHN4LCJAE7WEAEA2KF562XFAGDBOB64V"""

        op = proto.StellarPaymentOp()
        op.amount = 500111000
        op.destination_account = (
            "GBOVKZBEM2YYLOCDCUXJ4IMRKHN4LCJAE7WEAEA2KF562XFAGDBOB64V"
        )
        op.asset = proto.StellarAssetType(0)

        tx = self._create_msg()

        response = stellar.sign_tx(
            client, tx, [op], self.ADDRESS_N, self.NETWORK_PASSPHRASE
        )

        assert (
            b64encode(response.signature)
            == b"pDc6ghKCLNoYbt3h4eBw+533237m0BB0Jp/d/TxJCA83mF3o5Fr4l5vwAWBR62hdTWAP9MhVluY0cd5i54UwDg=="
        )

    @pytest.mark.setup_client(mnemonic=MNEMONIC12)
    def test_sign_tx_payment_op_custom_asset1(self, client):
        """Custom asset payment (code length 1) of 50.0111 X to GBOVKZBEM2YYLOCDCUXJ4IMRKHN4LCJAE7WEAEA2KF562XFAGDBOB64V"""

        op = proto.StellarPaymentOp()
        op.amount = 500111000
        op.destination_account = (
            "GBOVKZBEM2YYLOCDCUXJ4IMRKHN4LCJAE7WEAEA2KF562XFAGDBOB64V"
        )

        op.asset = proto.StellarAssetType(
            1, "X", "GAUYJFQCYIHFQNS7CI6BFWD2DSSFKDIQZUQ3BLQODDKE4PSW7VVBKENC"
        )
        tx = self._create_msg()

        response = stellar.sign_tx(
            client, tx, [op], self.ADDRESS_N, self.NETWORK_PASSPHRASE
        )

        assert (
            b64encode(response.signature)
            == b"ArZydOtXU2whoRuSjJLFIWPSIsq3AbsncJZ+THF24CRSriVWw5Fy/dHrDlUOu4fzU28I6osDMeI39aWezg5tDw=="
        )

    @pytest.mark.setup_client(mnemonic=MNEMONIC12)
    def test_sign_tx_payment_op_custom_asset12(self, client):
        """Custom asset payment (code length 12) of 50.0111 ABCDEFGHIJKL to GBOVKZBEM2YYLOCDCUXJ4IMRKHN4LCJAE7WEAEA2KF562XFAGDBOB64V"""

        op = proto.StellarPaymentOp()
        op.amount = 500111000
        op.destination_account = (
            "GBOVKZBEM2YYLOCDCUXJ4IMRKHN4LCJAE7WEAEA2KF562XFAGDBOB64V"
        )

        op.asset = proto.StellarAssetType(
            2,
            "ABCDEFGHIJKL",
            "GAUYJFQCYIHFQNS7CI6BFWD2DSSFKDIQZUQ3BLQODDKE4PSW7VVBKENC",
        )
        tx = self._create_msg()

        response = stellar.sign_tx(
            client, tx, [op], self.ADDRESS_N, self.NETWORK_PASSPHRASE
        )

        assert (
            b64encode(response.signature)
            == b"QZIP4XKPfe4OpZtuJiyrMZBX9YBzvGpHGcngdgFfHn2kcdONreF384/pCF80xfEnGm8grKaoOnUEKxqcMKvxAA=="
        )

    @pytest.mark.setup_client(mnemonic=MNEMONIC12)
    def test_sign_tx_set_options(self, client):
        """Set inflation destination"""

        op = proto.StellarSetOptionsOp()
        op.inflation_destination_account = (
            "GAFXTC5OV5XQD66T7WGOB2HUVUC3ZVJDJMBDPTVQYV3G3K7TUHC6CLBR"
        )

        tx = self._create_msg()
        response = stellar.sign_tx(
            client, tx, [op], self.ADDRESS_N, self.NETWORK_PASSPHRASE
        )

        assert (
            b64encode(response.signature)
            == b"dveWhKY8x7b0YqGHWH6Fo1SskxaHP11NXd2n6oHKGiv+T/LqB+CCzbmJA0tplZ+0HNPJbHD7L3Bsg/y462qLDA=="
        )

        op = proto.StellarSetOptionsOp()
        op.signer_type = 0
        op.signer_key = bytes.fromhex(
            "72187adb879c414346d77c71af8cce7b6eaa57b528e999fd91feae6b6418628e"
        )
        op.signer_weight = 2

        tx = self._create_msg()
        response = stellar.sign_tx(
            client, tx, [op], self.ADDRESS_N, self.NETWORK_PASSPHRASE
        )
        assert (
            b64encode(response.signature)
            == b"EAeihuFBhUnjH6Sgd/+uAHlvajfv944VEpNSCLsOULNxYWdo/S0lJdUZw/2kN6I+ztKL7ZPQ5gYPJRNUePTOCg=="
        )

        op = proto.StellarSetOptionsOp()
        op.medium_threshold = 0

        tx = self._create_msg()
        response = stellar.sign_tx(
            client, tx, [op], self.ADDRESS_N, self.NETWORK_PASSPHRASE
        )
        assert (
            b64encode(response.signature)
            == b"E2pz06PFB5CvIT3peUcY0wxo7u9da2h6/+/qim1eRWLHC73ZtFqDtLMBaKnr63ZfjB/kDzZmCzHxiv5m+m6+AQ=="
        )

        op = proto.StellarSetOptionsOp()
        op.low_threshold = 0
        op.high_threshold = 3
        op.clear_flags = 0

        tx = self._create_msg()
        response = stellar.sign_tx(
            client, tx, [op], self.ADDRESS_N, self.NETWORK_PASSPHRASE
        )
        assert (
            b64encode(response.signature)
            == b"ySQE4aS0TI+N1xjSwi/pABHpC+A6RrNPWDOuFYGJFQ5B4vIU2S+ql2gCGLE7bQiYZ5dK9021f+a30mZoYeFLDw=="
        )

        op = proto.StellarSetOptionsOp()
        op.set_flags = 3
        op.master_weight = 4
        op.home_domain = "hello"

        tx = self._create_msg()
        response = stellar.sign_tx(
            client, tx, [op], self.ADDRESS_N, self.NETWORK_PASSPHRASE
        )
        assert (
            b64encode(response.signature)
            == b"22rfcOrxBiE5akpNsnWX8yPgAOpclbajVqXUaXMNeL000p1OhFhi050t1+GNRpoSNyfVsJGNvtlICGpH4ksDAQ=="
        )

    def _create_msg(self) -> proto.StellarSignTx:
        tx = proto.StellarSignTx()
        tx.source_account = "GAK5MSF74TJW6GLM7NLTL76YZJKM2S4CGP3UH4REJHPHZ4YBZW2GSBPW"
        tx.fee = 100
        tx.sequence_number = 0x100000000
        tx.memo_type = 0
        return tx
