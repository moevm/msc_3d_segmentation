package ru.vorobyov.simplificationmethods.service.python;

public enum PythonMethods {
    ITERATIVE_METHOD(".iterative");

    private final String methodPath;
    private static final String PATH = ".path";

    PythonMethods(String value) {
        this.methodPath = PATH + value;
    }

    public String getMethodPath() {
        return methodPath;
    }
}
