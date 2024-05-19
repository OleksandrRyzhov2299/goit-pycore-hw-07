def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "🟡 Give me name and phone please."
        except KeyError:
            return "🟡 Contact does not exist"
        except IndexError:
            return "🟡 Enter contact name"
        except:
            return "🔴 Some error is occured. We are working on a solution"

    return inner