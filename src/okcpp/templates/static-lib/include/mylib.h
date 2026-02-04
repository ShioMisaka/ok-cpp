#ifndef MYLIB_H
#define MYLIB_H

#include <string>

namespace mylib {

class Calculator {
public:
    static int add(int a, int b);
    static int multiply(int a, int b);
};

std::string getVersion();

} // namespace mylib

#endif // MYLIB_H
