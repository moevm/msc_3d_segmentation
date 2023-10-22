package ru.vorobyov.simplificationmethods.configuration;

import ru.vorobyov.simplificationmethods.service.mongo.MongoModels;
import ru.vorobyov.simplificationmethods.service.python.PythonMethods;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

public class ApplicationConfiguration {
    private final static File PROPERTIES_PATH = new File("src/main/resources/application.properties").getAbsoluteFile();
    private final static Properties props;

    static {
        props = new Properties();
        try (FileInputStream propStream = new FileInputStream(PROPERTIES_PATH)) {
            props.load(propStream);
        } catch (IOException e) {
            throw new
                    RuntimeException("Не удалось найти расположение настроек приложения");
        }
    }

    public static String getProperty(ConfigurationFields field) {
        return props.getProperty(field.getFieldName());
    }

    public static String getModelProperty(ConfigurationFields field, MongoModels collection) {
        return props.getProperty(field.getFieldName() + collection.getFieldName());
    }

    public static String getMethodProperty(ConfigurationFields field, PythonMethods methods) {
        return props.getProperty(field.getFieldName() + methods.getMethodPath());
    }
}
