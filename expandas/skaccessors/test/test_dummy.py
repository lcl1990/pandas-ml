#!/usr/bin/env python

import numpy as np
import pandas as pd
import pandas.compat as compat

import sklearn.datasets as datasets
import sklearn.dummy as dummy

import expandas as expd
import expandas.util.testing as tm


class TestDummy(tm.TestCase):

    def test_objectmapper(self):
        df = expd.ModelFrame([])
        self.assertIs(df.dummy.DummyClassifier, dummy.DummyClassifier)
        self.assertIs(df.dummy.DummyRegressor, dummy.DummyRegressor)

    def test_Classifications(self):
        iris = datasets.load_iris()
        df = expd.ModelFrame(iris)

        models = ['DummyClassifier']
        for model in models:
            mod1 = getattr(df.dummy, model)(strategy='most_frequent',
                                            random_state=self.random_state)
            mod2 = getattr(dummy, model)(strategy='most_frequent',
                                         random_state=self.random_state)

            df.fit(mod1)
            mod2.fit(iris.data, iris.target)

            result = df.predict(mod1)
            expected = mod2.predict(iris.data)

            self.assertTrue(isinstance(result, expd.ModelSeries))
            self.assert_numpy_array_almost_equal(result.values, expected)

            self.assertEqual(df.score(mod1), mod2.score(iris.data, iris.target))


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
