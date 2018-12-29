drop trigger test on temp.templstrings;
drop function if exists temp.t_f_not();

CREATE FUNCTION temp.t_f_not()
RETURNS TRIGGER 
LANGUAGE plpgsql 
AS $$
BEGIN
     PERFORM pg_notify('test', format('%s', NEW.id));
     RETURN NEW;
END;
$$;

CREATE TRIGGER test AFTER INSERT OR UPDATE of geom ON temp.templstrings
    FOR EACH ROW EXECUTE PROCEDURE temp.t_f_not();