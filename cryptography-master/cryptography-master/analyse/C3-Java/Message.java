/**
 * Class that represents a message
 * It can be a raw message or a cyphered message
 * 
 * @author Nico
 */
public class Message {
    private byte[][] byteMessage;
    private String message;

    /**
     * Constructor that builds a Message from a string
     * 
     * @param message
     */
    public Message(String message) {
        this.message = message;
        this.byteMessage = Utils.toDoubleByte(message);
    }

    /**
     * Constructor that builds a Message from a byte array
     * 
     * @param byteMessage
     */
    public Message(byte[][] byteMessage) {
        this.byteMessage = byteMessage;
        message = "";
        for (int i = 0; i < byteMessage.length; i++) {
            message += (char) (((byteMessage[i][0] & 0xff)) << 8 | (byteMessage[i][1] & 0xff));
        }
    }

    /**
     * Print functions
     */
    public void printByteMessage() {
        for (int i = 0; i < byteMessage.length; i++) {
            String s1 = String.format("%8s", Integer.toBinaryString(byteMessage[i][0] & 0xFF)).replace(' ', '0');
            String s2 = String.format("%8s", Integer.toBinaryString(byteMessage[i][1] & 0xFF)).replace(' ', '0');
            System.out.println("x" + String.valueOf(i) + ": " + s1 + " " + s2);
        }
    }

    public void printMessage() {
        System.out.println("Message : " + message);
    }

    /**
     * Getter
     * 
     * @return the message
     */
    public String getMessage() {
        return message;
    }

    /**
     * Getter
     * 
     * @return the byte array
     */
    public byte[][] getBytes() {
        return byteMessage;
    }
}
