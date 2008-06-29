# Copyright (C) 2007 Samuel Abels, http://debain.org
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
from SpiffWorkQueue import Action

True  = 1
False = 0

class CommandScript(Action):
    def __init__(self, exscript):
        assert exscript is not None
        Action.__init__(self)
        self.exscript = exscript


    def _on_data_received(self, *args):
        self.signal_emit('data_received', *args)


    def execute(self, global_lock, global_data, local_data):
        assert global_lock is not None
        assert global_data is not None
        assert local_data  is not None
        local_data['transport'].set_on_data_received_cb(self._on_data_received)
        self.exscript.define(__connection__ = local_data['transport'])
        self.exscript.define(__user__       = local_data['user'])
        self.exscript.execute()
        local_data['transport'].set_on_data_received_cb(None)
        return True
