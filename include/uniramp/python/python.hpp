#pragma once

/*
 * Copyright (c) 2021, Cycatz <cycatz@staque.xyz>
 * BSD-style license; see COPYING
 */

#include <pybind11/pybind11.h> // Must be the first include.
#include <pybind11/stl.h>
#include <uniramp/uniramp.hpp>

namespace uniramp
{

namespace python
{
    /* ref: https://pybind11.readthedocs.io/en/stable/classes.html */
    void initialize(pybind11::module &mod)
    {
        namespace py = pybind11;
    }

} /* end namespace python */

} /* end namespace uniramp */
