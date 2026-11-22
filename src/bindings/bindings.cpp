
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "cartpole/controllers/StateFeedbackController.h"

namespace py = pybind11;

PYBIND11_MODULE(cartpole_control, m)
{
    py::class_<StateFeedbackController>(m, "StateFeedbackController")
        .def(py::init<>())
        .def("setGains", &StateFeedbackController::setGains)
        .def("computeControlInput", &StateFeedbackController::computeControlInput);
}
