'''
quantus: Slave test module

Meant for use with py.test.
Write each test as a function named test_<something>.
Read more here: http://pytest.org/

Copyright 2014, Andrew Trask
Licensed under Apache
'''

from quantus.slave.Slave import Slave
import numpy
import pytest


class TestSlave:

    @pytest.fixture
    def empty_slave(self):
        return Slave()

    @pytest.fixture
    def slave(self, empty_slave):
        empty_slave.createSubVector(10)
        return empty_slave

    def test_sanity(self):
        assert 1 + 1 == 2

    def test_create_vector(self, empty_slave):
        empty_slave.createSubVector(10)
        assert len(empty_slave.subvectors) == 1

    @pytest.mark.parametrize("value", [0, 1, -1, 100, 1000])
    def test_scalar_add(self, slave, value):
        message = "subvector:iadd:0:{0}".format(value)
        slave.parse(message)
        expected = numpy.zeros(10) + value

        assert numpy.array_equal(slave.subvectors[0].data, expected)

    @pytest.mark.parametrize("value", [0, 1, -1, 100, 1/3])
    def test_scalar_mult(self, slave, value):
        slave.subvectors[0].iadd(1)
        message = "subvector:imul:0:{0}".format(value)
        slave.parse(message)
        expected = numpy.ones(10) * value

        assert numpy.array_equal(slave.subvectors[0].data, expected)


    @pytest.mark.parametrize("value", [0, 1, -1, 100, 1/3, 1/2])
    def test_scalar_div(self, slave, value):
        slave.subvectors[0].iadd(1)
        message = "subvector:div:0:{0}".format(value)
        slave.parse(message)
        expected = numpy.ones(10) / value

        assert numpy.array_equal(slave.subvectors[0].data, expected)

    @pytest.mark.parametrize("value", [0, 1, 2])
    def test_dot(self, empty_slave, value):
        """
        Use Slave to take the dot product of a ones array with an array of ones, an array of twos,
        and an array of threes

        :param empty_slave: Slave object with no SubVectors
        :param value: index of SubVector to dot product with SubVector 0
        """
        empty_slave.createSubVector(10)
        empty_slave.createSubVector(10)
        empty_slave.createSubVector(10)
        # ones, twos, threes
        for i, sv in enumerate(empty_slave.subvectors):
            sv.iadd(1 + i)

        message = "subvector:dot:0:{0}".format(value)
        actual = float(empty_slave.parse(message))
        expected = numpy.ones(10).dot(numpy.ones(10) + value)

        assert actual == expected

    @pytest.mark.parametrize("value", [0, 1, 2])
    def test_elementwise_mult(self, empty_slave, value):
        """
        Use Slave to take SubVectors and multiply elementwise

        :param empty_slave: Slave object with no SubVectors
        :param value: index of SubVector to multiply with SubVector 0
        """
        empty_slave.createSubVector(10)
        empty_slave.createSubVector(10)
        empty_slave.createSubVector(10)
        # ones, twos, threes
        for i, sv in enumerate(empty_slave.subvectors):
            sv.iadd(1 + i)

        message = "subvector:imulVec:0:{0}".format(value)
        empty_slave.parse(message)
        expected = numpy.ones(10) * (numpy.ones(10) + value)

        assert numpy.array_equal(empty_slave.subvectors[0].data, expected)

    @pytest.mark.parametrize("value", [0, 1, 2])
    def test_elementwise_div(self, empty_slave, value):
        """
        Use Slave to take SubVectors and divide elementwise

        :param empty_slave: Slave object with no SubVectors
        :param value: index of SubVector to divide with SubVector 0
        """
        empty_slave.createSubVector(10)
        empty_slave.createSubVector(10)
        empty_slave.createSubVector(10)
        # ones, twos, threes
        for i, sv in enumerate(empty_slave.subvectors):
            sv.iadd(1 + i)
        message = "subvector:divVec:0:{0}".format(value)
        empty_slave.parse(message)
        expected = numpy.ones(10) / (numpy.ones(10) + value)

        assert numpy.array_equal(empty_slave.subvectors[0].data, expected)

    @pytest.mark.parametrize("value", [0, 1, 2])
    def test_elementwise_add(self, empty_slave, value):
        """
        Use Slave to take SubVectors and add elementwise

        :param empty_slave: Slave object with no SubVectors
        :param value: index of SubVector to add with SubVector 0
        """
        empty_slave.createSubVector(10)
        empty_slave.createSubVector(10)
        empty_slave.createSubVector(10)
        # ones, twos, threes
        for i, sv in enumerate(empty_slave.subvectors):
            sv.iadd(1 + i)
        message = "subvector:iaddVec:0:{0}".format(value)
        empty_slave.parse(message)
        expected = numpy.ones(10) + (numpy.ones(10) + value)

        assert numpy.array_equal(empty_slave.subvectors[0].data, expected)

    @pytest.mark.parametrize("value", [0, 1, -1, 100, 1/3, 1/2])
    def test_pow(self, slave, value):
        slave.subvectors[0].iadd(8)
        message = "subvector:pow:0:{0}".format(value)
        slave.parse(message)
        expected = (numpy.ones(10) * 8) ** value

        assert numpy.array_equal(slave.subvectors[0].data, expected)

    @pytest.mark.parametrize("value", [0, 1, -1, 100, 1/3])
    def test_sum(self, slave, value):
        slave.subvectors[0].iadd(value)
        message = "subvector:sum:0"
        actual = float(slave.parse(message))
        expected = sum(numpy.ones(10) * value, 0)

        assert actual == expected

    def test_randn(self, slave):
        """
        Baseline check to make sure the function executes
        """
        slave.subvectors[0].iadd(1)
        message = "subvector:randn:0:1"
        exit_code = slave.parse(message)
        assert exit_code == '0'

    def test_uniform(self, slave):
        """
        Baseline check to make sure the function executes
        """
        slave.subvectors[0].iadd(1)
        message = "subvector:uniform:0:1"
        exit_code = slave.parse(message)
        assert exit_code == '0'

