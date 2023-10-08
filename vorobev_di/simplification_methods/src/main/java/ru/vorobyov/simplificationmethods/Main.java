package ru.vorobyov.simplificationmethods;

import ru.vorobyov.simplificationmethods.algorithm.GeometricSimplification;

public class Main {
    public static void main(String[] args) {
        /*if (args.length < 3)
            throw new IllegalArgumentException("Введено менее 3-х аргументов");*/

        long start = System.currentTimeMillis();

        GeometricSimplification geometricSimplification = new GeometricSimplification(36);
        geometricSimplification.process();

        double elapsedTimeInSec = (System.currentTimeMillis() - start) ;

        System.out.println("Готово!");
        System.out.println("Затрачено времени в мс: " + elapsedTimeInSec);

    }
}
