 const float e = 115.0;     // end effector
 const float f = 350;     // base
 const float re = 300.0;
 const float rf = 170.0;
 
 // trigonometric constants
 const float sqrt3 = sqrt(3.0);
 const float pi = 3.141592653;    // PI
 const float sin120 = sqrt3/2.0;   
 const float cos120 = -0.5;        
 const float tan60 = sqrt3;
 const float sin30 = 0.5;
 const float tan30 = 1/sqrt3;


int delta_calcAngleYZ(float x0, float y0, float z0, float &theta) {
     float y1 = -0.5 * 0.57735 * f; // f/2 * tg 30
     y0 -= 0.5 * 0.57735    * e;    // shift center to edge
     // z = a + b*y
     float a = (x0*x0 + y0*y0 + z0*z0 +rf*rf - re*re - y1*y1)/(2*z0);
     float b = (y1-y0)/z0;
     // discriminant
     float d = -(a+b*y1)*(a+b*y1)+rf*(b*b*rf+rf); 
     if (d < 0) return -1; // non-existing point
     float yj = (y1 - a*b - sqrt(d))/(b*b + 1); // choosing outer point
     float zj = a + b*yj;
     theta = 180.0*atan(-zj/(y1 - yj))/pi + ((yj>y1)?180.0:0.0);
     return 0;
 }
 
 // inverse kinematics: (x0, y0, z0) -> (theta1, theta2, theta3)
 // returned status: 0=OK, -1=non-existing position
 void delta_calcInverse(float x0, float y0, float z0, float thetas[]) {
     thetas[0] = thetas[1] = thetas[2] = 0;
     int status = delta_calcAngleYZ(x0, y0, z0, thetas[0]);
        Serial.println(status);

     if (status == 0) status = delta_calcAngleYZ(x0*cos120 + y0*sin120, y0*cos120-x0*sin120, z0, thetas[1]);  // rotate coords to +120 deg
     if (status == 0) status = delta_calcAngleYZ(x0*cos120 - y0*sin120, y0*cos120+x0*sin120, z0, thetas[2]);  // rotate coords to -120 deg
 }

    int stepn[3];
    int stepo[3];
void theta_step(float thetas[] ,int steps[]){
  for (int i=0;i<3;i++){
    steps[i]=stepo[i];
    stepn[i]=round(thetas[i]*(3200*5/360));
    steps[i]=stepn[i]-steps[i];
    stepo[i]=stepn[i];
    }
 }


void axis2step(float x0, float y0, float z0,int &step1, int &step2, int &step3){

    thetas[0] = thetas[1] = thetas[2] = 0;
    int status = delta_calcAngleYZ(x0, y0, z0, thetas[0]);
    if (status == 0) status = delta_calcAngleYZ(x0*cos120 + y0*sin120, y0*cos120-x0*sin120, z0, thetas[1]);  // rotate coords to +120 deg
    if (status == 0) status = delta_calcAngleYZ(x0*cos120 - y0*sin120, y0*cos120+x0*sin120, z0, thetas[2]);  // rotate coords to -120 deg
    for (int i=0;i<3;i++){
        steps[i]=stepo[i];
        stepn[i]=round(thetas[i]*(3200*5/360));
        steps[i]=stepn[i]-steps[i];
        stepo[i]=stepn[i];
    }

    // float theta1 = theta2 = theta3 = 0;
    // int status = delta_calcAngleYZ(x0, y0, z0, theta1);
    // if (status == 0) status = delta_calcAngleYZ(x0*cos120 + y0*sin120, y0*cos120-x0*sin120, z0, theta2);  // rotate coords to +120 deg
    // if (status == 0) status = delta_calcAngleYZ(x0*cos120 - y0*sin120, y0*cos120+x0*sin120, z0, theta3);  // rotate coords to -120 deg
    // int stepn1;
    // int stepn2;
    // int stepn3;

    // stepn1=round(theta1*(3200/360));
    // step1=stepn1-step1;

    // stepn2=round(theta2*(3200/360));
    // step2=stepn2-step2;

    // stepn3=round(theta3*(3200/360));
    // step3=stepn3-step3;
}

