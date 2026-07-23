PASSWORD_MIN_LENGTH = 8
# bcrypt silently ignores/rejects input past 72 bytes — capping here so the
# error is a clean 422 at the API boundary instead of a 500 from bcrypt.
PASSWORD_MAX_LENGTH = 72