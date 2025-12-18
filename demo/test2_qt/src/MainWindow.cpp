#include "MainWindow.h"

#include <QDebug>

MainWindow::MainWindow(QWidget* parent)
 : QMainWindow(parent)
{
    setWindowTitle("Hello");
    setGeometry(1000, 500, 500, 500);

    QWidget *mainWidget = new QWidget(this);
    setCentralWidget(mainWidget);

    // QVBoxLayout *vlayout = new QVBoxLayout(mainWidget);
    // mainWidget->setLayout(vlayout);

}

MainWindow::~MainWindow()
{

}