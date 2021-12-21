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
        .def(py::init<const std::string &, signed long>(), py::arg("font_path"),
             py::arg("face_index") = 0)
        .def("num_glyph", &Typeface::num_glyph)
        .def("get_pixel_size", &Typeface::get_pixel_size)
        .def("set_pixel_size", &Typeface::set_pixel_size)
        .def("get_family_name", &Typeface::get_family_name)
        .def("get_style_name", &Typeface::get_style_name)
        .def("get_coverage", &Typeface::get_coverage);
}

} /* end namespace python */

} /* end namespace uniramp */
