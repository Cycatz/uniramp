/*
 * Copyright (c) 2021, Cycatz <cycatz@staque.xyz>
 * BSD-style license; see COPYING
 */

#include <uniramp/python/python.hpp>  // Must be the first include.
#include <uniramp/uniramp.hpp>

PYBIND11_MODULE(_uniramp, mod)  // NOLINT
{
    uniramp::python::initialize(mod);
}
