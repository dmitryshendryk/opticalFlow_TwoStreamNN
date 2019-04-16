
#include "../opt_flow.hpp"
#include <boost/python.hpp>

BOOST_PYTHON_MODULE(cOptical)
{
    using namespace boost::python;
    

    class_<OpticalFlow>("OpticalFlow")
        .def("compute_Flow", &OpticalFlow::compute_Flow)
        .def("test_print",  &OpticalFlow::test_print)
        .def("test_camera", &OpticalFlow::test_camera);
}