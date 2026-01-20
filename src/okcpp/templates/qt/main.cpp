// main.cpp
#include <iostream>

#include <QApplication>
#include <QMainWindow>

#include "MainWindow.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    MainWindow w;
    w.show();
    std::cout << "QT Windows is Run..." << std::endl;
    return app.exec();
}
