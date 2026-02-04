#include <iostream>
#include "mylib.h"

int main() {
    using namespace mylib;

    std::cout << "=== Dynamic Library Test ===" << std::endl;
    std::cout << "MyLib Version: " << getVersion() << std::endl;
    std::cout << "5 + 3 = " << Calculator::add(5, 3) << std::endl;
    std::cout << "5 * 3 = " << Calculator::multiply(5, 3) << std::endl;

    return 0;
}
