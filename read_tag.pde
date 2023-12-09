import themidibus.*;

MidiBus bus;
int tag[] = new int[4];

void setup() {
  MidiBus.list();
  // 1 -> numero dans liste des input
  //MidiBus(java.lang.Object parent, int in_device_num, int out_device_num)
  bus = new MidiBus(this, 1,2);
  bus.sendNoteOff(new Note(0,64,127));
}

void draw() {
  
}

void controllerChange(int channel, int number, int value) {
    switch(number) {
      case 7:
        tag[floor(number/2)] += value;
        println("uuid :",hex(tag[0],2),hex(tag[1],2),hex(tag[2],2),hex(tag[3],2));
        break;
      default:
        //println(number,value,hex(value),"générique");
        if (number%2 == 0) { // debut de chiffre
          tag[floor(number/2)] = value*128;
        } else {
          tag[floor(number/2)] += value;
        }
    }
    //resetMotif();
}
