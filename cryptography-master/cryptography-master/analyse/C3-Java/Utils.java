/**
 * Useful functions
 * 
 * @author Nico
 */
public class Utils {

    /**
     * Converts a string into double byte format
     * 
     * @param message
     * @return a byte array
     */
    public static byte[][] toDoubleByte(String message) {
        try {
            byte[][] byteMessage = new byte[message.length()][2];

            byte[] b = message.getBytes("UTF-16");
            for (int i = 2; i < b.length; i++) {
                if (i % 2 == 0) {
                    byteMessage[(i - 2) / 2][0] = b[i];
                } else {
                    byteMessage[(i - 2) / 2][1] = b[i];
                }
            }

            return byteMessage;
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }

        return null;
    }

    public static byte xor(byte b1, byte b2) {
        return (byte) ((0xff & (((int) b1) ^ ((int) b2))));
    }
}
