DO $$ BEGIN -- Load States
    BEGIN COPY public.survey_state(id, name, country)
        FROM 'states.csv' DELIMITER ',' CSV HEADER;
        RAISE NOTICE 'States loaded successfully';
        EXCEPTION
        WHEN OTHERS THEN RAISE WARNING 'Error loading states: %',
        SQLERRM;
        ROLLBACK;
    END;
    -- Load Districts
    BEGIN COPY public.survey_district(id, name, state)
        FROM 'districts.csv' DELIMITER ',' CSV HEADER;
        RAISE NOTICE 'Districts loaded successfully';
        EXCEPTION
        WHEN OTHERS THEN RAISE WARNING 'Error loading districts: %',
        SQLERRM;
        ROLLBACK;
    END;
    -- Load Talukas
    BEGIN COPY public.survey_taluka(id, name, district) FROM 'talukas.csv' DELIMITER ',' CSV HEADER;
        RAISE NOTICE 'Talukas loaded successfully';
        EXCEPTION
        WHEN OTHERS THEN RAISE WARNING 'Error loading talukas: %',
        SQLERRM;
        ROLLBACK;
        END;
END $$;