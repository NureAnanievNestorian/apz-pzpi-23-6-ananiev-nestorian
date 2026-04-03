interface Mediator {
  void notify(Component sender, String event);
}

class ConcreteMediator implements Mediator {
  private Button button;
  private TextBox textBox;

  public ConcreteMediator(Button b, TextBox t) {
      this.button = b;
      this.textBox = t;
  }

  @Override
  public void notify(Component sender, String event) {
      if (sender == button && event.equals("click")) {
          textBox.setText("Натиснуто кнопку");
      }
  }
}

abstract class Component {
  protected Mediator mediator;
  public Component(Mediator m) {
      this.mediator = m;
  }
}

class Button extends Component {
  public Button(Mediator m) {
      super(m);
  }
  public void click() {
      mediator.notify(this, "click");
  }
}

class TextBox extends Component {
  private String text = "";
  public TextBox(Mediator m) {
      super(m);
  }
  public void setText(String t) {
      this.text = t;
  }
  public String getText() {
      return this.text;
  }
}

// Демонстрація використання
public class Main {
  public static void main(String[] args) {
      ConcreteMediator mediator = new ConcreteMediator(
          new Button(null), new TextBox(null)
      );
      Button btn = new Button(mediator);
      TextBox box = new TextBox(mediator);
      btn.click();
  }
}