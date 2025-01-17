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

import pytest

from trezorlib import messages as proto, stellar
from trezorlib.tools import CallException, parse_path

from .common import MNEMONIC12, TrezorTest
from .conftest import TREZOR_VERSION


@pytest.mark.altcoin
@pytest.mark.stellar
class TestMsgStellarGetAddress(TrezorTest):
    @pytest.mark.setup_client(mnemonic=MNEMONIC12)
    def test_stellar_get_address(self, client):
        address = stellar.get_address(client, parse_path(stellar.DEFAULT_BIP32_PATH))
        assert address == "GAK5MSF74TJW6GLM7NLTL76YZJKM2S4CGP3UH4REJHPHZ4YBZW2GSBPW"

    @pytest.mark.setup_client(
        mnemonic="illness spike retreat truth genius clock brain pass fit cave bargain toe"
    )
    def test_stellar_get_address_sep(self, client):
        # data from https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0005.md
        address = stellar.get_address(client, parse_path(stellar.DEFAULT_BIP32_PATH))
        assert address == "GDRXE2BQUC3AZNPVFSCEZ76NJ3WWL25FYFK6RGZGIEKWE4SOOHSUJUJ6"

        address = stellar.get_address(
            client, parse_path("m/44h/148h/1h"), show_display=True
        )
        assert address == "GBAW5XGWORWVFE2XTJYDTLDHXTY2Q2MO73HYCGB3XMFMQ562Q2W2GJQX"

    def test_stellar_get_address_fail(self, client):
        with pytest.raises(CallException) as exc:
            stellar.get_address(client, parse_path("m/0/1"))

        if TREZOR_VERSION == 1:
            assert exc.value.args[0] == proto.FailureType.ProcessError
            assert exc.value.args[1].endswith("Failed to derive private key")
        else:
            assert exc.value.args[0] == proto.FailureType.DataError
            assert exc.value.args[1].endswith("Forbidden key path")
