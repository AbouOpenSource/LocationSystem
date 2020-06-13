//
// Created by abou on 09/06/2020.
//

#include "Position.h"
Position *Position::instance = nullptr;
Position::Position(double x, double y, double z) : x(x), y(y), z(z) {
}

double Position::getX() const {
    return x;
}

double Position::getY() const {
    return y;
}

double Position::getZ() const {
    return z;
}

void Position::setX(double x_) {
    Position::x = x_;
}

void Position::setY(double y_) {
    Position::y = y_;
}

void Position::setZ(double z_) {
    Position::z = z_;
}

Position::Position() {
    Position::x =1;
    Position::y =2;
    Position::z =3;
}

Position *Position::getMyPosition() {
    if (!instance)
        instance = new Position;
    return instance;
}
