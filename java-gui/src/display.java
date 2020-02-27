import javax.swing.*;
import java.awt.*;

public class display {

  public static void main(String[] args){
    initGUI();

  }

  public static void initGUI(){

    /*
    GraphicsEnvironment ge = GraphicsEnvironment.getLocalGraphicsEnvironment();
    GraphicsDevice[] gs = ge.getScreenDevices();

    // Get size of each screen

    for (int i=0; i<gs.length; i++) {
        DisplayMode dm = gs[i].getDisplayMode();
        int screenWidth = dm.getWidth();
        int screenHeight = dm.getHeight();
      }
    */


    JFrame f = new JFrame("Azure Maze");

    f.setAlwaysOnTop(true);
    f.setExtendedState(JFrame.MAXIMIZED_BOTH);
    f.setUndecorated(true);

    f.setVisible(true);
  }
}
