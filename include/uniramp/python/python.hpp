/*
 * Copyright (c) 2021, Cycatz <cycatz@staque.xyz>
 * BSD-style license; see COPYING
 */

#pragma once

#include <pybind11/pybind11.h>  // Must be the first include.
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
    py::class_<Typeface>(mod, "Typeface")
        .def(py::init<const std::string &>())
        .def("num_glyph", &Typeface::num_glyph)
        .def("get_coverage", &Typeface::get_coverage);
}

} /* end namespace python */

} /* end namespace uniramp */
