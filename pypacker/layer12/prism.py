"""
Prism header.
This packet type exists just for convenience. Radiotap should be prefered over prism
because of its superior flexibility. Only use this if there is no support for Radiotap
eg for some Broadcom-Chipsets (stop buying crap man).
"""

from pypacker import pypacker, triggerlist
from pypacker.layer12.ieee80211 import IEEE80211

import logging
import struct

logger = logging.getLogger("pypacker")


PRISM_TYPE_80211	= 0

PRISM_DID_RSSI		= 0x41400000

class Did(pypacker.Packet):
	__hdr__ = (
		("id", "I", 0),
		("status", "H", 0),
		("len", "H", 0),
		("value", "I", 0),
		)

	__byte_order__ = "<"



class Prism(pypacker.Packet):
	__hdr__ = (
		("code", "I", 0),
		("len", "I", 144),
		("dev", "16s", b""),
		("dids", None, triggerlist.TriggerList),
		)

	def _dissect(self, buf):
		off = 24
		# assume 10 DIDs, 24 + 10*12 = 144 bytes prism header
		end = off + 10*12

		dids = []

		while off < end:
			did = Did( buf[off:off+12])
			dids.append(did)
			off += 12

		self.dids.extend(dids)
		self._parse_handler(PRISM_TYPE_80211, buf, 144)


# load handler
from pypacker.layer12 import ieee80211

pypacker.Packet.load_handler(Prism,
				{
				PRISM_TYPE_80211 : ieee80211.IEEE80211
				}
			)
