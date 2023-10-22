package ru.vorobyov.simplificationmethods.algorithm;

import java.util.Arrays;

public enum AlgorithmTypes {
    BASIC("-b"),
    GEOMETRIC("-g"),
    ITERATIVE("-i");

    private final String flag;

    AlgorithmTypes(String value) {
        this.flag = value;
    }

    public static AlgorithmTypes getFromFlag(String flag){
        return Arrays.stream(AlgorithmTypes.values())
                .filter(x -> x.flag.equals(flag))
                .findFirst()
                .orElseThrow(() -> new IllegalArgumentException("По указанному флагу алгоритм не найден!"));
    }
}
