package io.github.ilovejackylee.goldkaratvalue;

public final class CalcException extends RuntimeException {
    private final CalcError error;

    public CalcException(CalcError error, String message) {
        super(message);
        this.error = error;
    }

    public CalcError getError() {
        return error;
    }
}
