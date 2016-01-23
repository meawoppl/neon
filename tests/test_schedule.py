# ----------------------------------------------------------------------------
# Copyright 2015 Nervana Systems Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------
import numpy as np

from neon.optimizers import Schedule, ExpSchedule


def test_step_schedule(backend_default):
    """
    Test constant rate, fixed step and various modes of programmable steps.
    """
    lr_init = 0.1

    # default scheduler has a constant learning rate
    sch = Schedule()
    for epoch in range(10):
        lr = sch.get_learning_rate(learning_rate=lr_init, epoch=epoch)
        assert lr == lr_init

    # test a uniform step schedule
    step_config = 2
    change = 0.5
    sch = Schedule(step_config=step_config, change=change)
    for epoch in range(10):
        lr = sch.get_learning_rate(learning_rate=lr_init, epoch=epoch)
        # test a repeated call for the same epoch
        lr2 = sch.get_learning_rate(learning_rate=lr_init, epoch=epoch)
        # print(epoch, lr, lr2)
        assert np.allclose(lr, lr_init * change**(np.floor((epoch+1)/step_config)))
        assert np.allclose(lr2, lr_init * change**(np.floor((epoch+1)/step_config)))

    # test a list step schedule
    sch = Schedule(step_config=[2, 3], change=.1)
    assert np.allclose(.1, sch.get_learning_rate(learning_rate=.1, epoch=0))
    assert np.allclose(.1, sch.get_learning_rate(learning_rate=.1, epoch=1))
    assert np.allclose(.01, sch.get_learning_rate(learning_rate=.1, epoch=2))
    # test a repeated call for the same epoch
    assert np.allclose(.01, sch.get_learning_rate(learning_rate=.1, epoch=2))
    assert np.allclose(.001, sch.get_learning_rate(learning_rate=.1, epoch=3))
    assert np.allclose(.001, sch.get_learning_rate(learning_rate=.1, epoch=4))


def test_exp_schedule(backend_default):
    """
    Test exponential learning rate schedule
    """
    lr_init = 0.1
    decay = 0.01
    sch = ExpSchedule(decay)
    for epoch in range(10):
        lr = sch.get_learning_rate(learning_rate=lr_init, epoch=epoch)
        assert np.allclose(lr, lr_init / (1. + decay * epoch))
