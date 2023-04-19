import java.math.BigInteger;

public class Polynomial {
    private int degree;
    private int[] coeff;

    /**
     * 
     * @param generate an array with p and coeffs from X
     * @param s        the secret
     */
    public Polynomial(int[] generate, int s) {
        degree = generate.length - 1;
        coeff = new int[generate.length];
        coeff[0] = s;
        for (int i = 1; i < generate.length; i++) {
            coeff[i] = generate[i];
        }
    }

    public Polynomial(int degree, int... coeff) {
        this.degree = degree;
        this.coeff = new int[degree + 1];
        for (int i = 0; i < coeff.length; i++) {
            this.coeff[i] = coeff[i];
        }
    }

    public BigInteger eval(int value,int prime) {
        BigInteger result = BigInteger.ZERO;
        BigInteger valPower = BigInteger.ONE;
        BigInteger Big_prime = BigInteger.valueOf(prime);
        for (int i = 0; i < coeff.length; i++) {
            BigInteger i_term = BigInteger.valueOf(coeff[i]); // coeff[i]
            i_term = i_term.multiply(valPower).mod(Big_prime); // coeff[i] * val^i
            result = result.add(i_term).mod(Big_prime); 
            valPower = valPower.multiply(BigInteger.valueOf(value)).mod(Big_prime); // increment exponant
        }
        return result;
    }

    public void add(Polynomial p) {
        if (p.degree < this.degree) {
            for (int i = 0; i < p.coeff.length; i++) {
                this.coeff[i] += p.coeff[i];
            }
        } else {
            for (int i = 0; i < this.coeff.length; i++) {
                p.coeff[i] += this.coeff[i];
                this.coeff = p.coeff;
                this.degree = p.degree;
            }
        }
    }

    public void sub(int s) {
        coeff[0] -= s;
    }

    public Polynomial mul(Polynomial p) {
        Polynomial result = new Polynomial(this.degree + p.degree);
        for (int i = 0; i < result.coeff.length; i++) {
            for (int j = 0; j < i + 1; j++) {
                int a = j > this.degree ? 0 : this.coeff[j];
                int b = i - j > p.degree ? 0 : p.coeff[i - j];
                result.coeff[i] += a * b;
            }
        }
        return result;
    }

    public void divide(int d) {
        for (int i = 0; i < coeff.length; i++) {
            coeff[i] = coeff[i] / d;
        }
    }

    @Override
    public String toString() {
        String s = "";
        if (coeff.length == 0)
            return s;

        s += String.valueOf(coeff[0]);

        for (int i = 1; i < coeff.length; i++) {
            s += " + " + String.valueOf(coeff[i]) + "X^" + String.valueOf(i);
        }

        return s;
    }
}