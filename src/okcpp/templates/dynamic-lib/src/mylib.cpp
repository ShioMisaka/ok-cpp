#include "mylib.h"

namespace mylib {

int Calculator::add(int a, int b) {
    return a + b;
}

int Calculator::multiply(int a, int b) {
    return a * b;
}

std::string getVersion() {
    return "1.0.0";
}

} // namespace mylib
