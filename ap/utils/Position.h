//
// Created by abou on 09/06/2020.
//

#ifndef APNEW_POSITION_H
#define APNEW_POSITION_H


class Position {
private:
    static Position* instance;
    double x;
    double y;
    double z;
public:
    Position();

    Position(double x, double y, double z);

    double getX() const;

    double getY() const;

    double getZ() const;

    void setX(double x);

    void setY(double y);

    void setZ(double z);

    static Position * getMyPosition();

    void changePosition() const{
        Position::instance->setX(Position::getX()+1);
        Position::instance->setY(Position::getX()+1);
        Position::instance->setZ(Position::getX()+1);

    }
};


#endif //APNEW_POSITION_H
