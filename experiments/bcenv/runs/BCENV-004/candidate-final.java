package tempest;
import battlecode.common.*;

public strictfp class RobotPlayer {
 static RobotController rc;
 static Team team, enemy;
 static int width,height,seed,age,hqIndex=-1,carriersBuilt,launchersBuilt,lastAnchorRound=-999;
 static MapLocation home,goal,well;
 static ResourceType mine;
 static int[] visited=new int[3600];
 static MapLocation[] knownIslands=new MapLocation[36];
 static int[] islandTeam=new int[36];
 static int[] islandSeen=new int[36];
 static MapLocation navTarget;
 static int navBest=999999,navStall=0,wallHit,wallSteps;
 static Direction wallDir;
 static boolean wallMode;
 static MapLocation[] knownWells=new MapLocation[32];
 static int[] wellType=new int[32];
 static int wellsCount=0;
 static Direction[] dirs={Direction.NORTH,Direction.NORTHEAST,Direction.EAST,Direction.SOUTHEAST,Direction.SOUTH,Direction.SOUTHWEST,Direction.WEST,Direction.NORTHWEST};
 static int random(int n){seed=seed*1664525+1013904223; return (seed>>>1)%n;}
 static int enc(MapLocation p){return 1+p.x+60*p.y;}
 static MapLocation dec(int n){n=(n&4095)-1;return n<0?null:new MapLocation(n%60,n/60);}
 static int dist(MapLocation a,MapLocation b){return a.distanceSquaredTo(b);}
 static void write(int i,int v)throws GameActionException{if(rc.canWriteSharedArray(i,v))rc.writeSharedArray(i,v);}
 public static void run(RobotController controller) {
  rc=controller;team=rc.getTeam();enemy=team.opponent();width=rc.getMapWidth();height=rc.getMapHeight();seed=rc.getID()*137+17;
  mine=rc.getID()%4==0?ResourceType.ADAMANTIUM:ResourceType.MANA;
  while(true){try{age++; observe();switch(rc.getType()){
   case HEADQUARTERS: headquarters();break;
   case CARRIER: carrier();break;
   case LAUNCHER: launcher();break;
   default:explore();break;
  }}catch(Exception e){System.out.println("ERR "+rc.getID()+" "+e.getMessage());}Clock.yield();}
 }
 static void observe()throws GameActionException{
  MapLocation p=rc.getLocation();visited[p.x+60*p.y]=rc.getRoundNum();
  if(rc.getType()==RobotType.HEADQUARTERS){home=p;if(hqIndex<0)for(int i=0;i<4;i++)if(rc.readSharedArray(i)==0||rc.readSharedArray(i)==enc(p)){hqIndex=i;write(i,enc(p));break;}}
  if(home==null){int best=99999;for(int i=0;i<4;i++){MapLocation h=dec(rc.readSharedArray(i));if(h!=null&&dist(p,h)<best){best=dist(p,h);home=h;}}}
  for(RobotInfo r:rc.senseNearbyRobots(-1,team))if(r.type==RobotType.HEADQUARTERS&&(home==null||dist(p,r.location)<dist(p,home)))home=r.location;
  for(WellInfo w:rc.senseNearbyWells()){
   MapLocation loc=w.getMapLocation();boolean exists=false;for(int i=0;i<wellsCount;i++)if(knownWells[i].equals(loc)){exists=true;break;}
   if(!exists&&wellsCount<32){knownWells[wellsCount]=loc;wellType[wellsCount++]=w.getResourceType()==ResourceType.ADAMANTIUM?1:2;}
  }
  for(int id:rc.senseNearbyIslands()){
   MapLocation[] ls=rc.senseNearbyIslandLocations(id);if(ls.length>0&&id<36){knownIslands[id]=ls[0];islandSeen[id]=rc.getRoundNum();Team t=rc.senseTeamOccupyingIsland(id);islandTeam[id]=t==team?1:t==enemy?2:0;}
  }
  if(rc.canWriteSharedArray(0,rc.readSharedArray(0))){
   for(int k=0;k<wellsCount;k++){
    int val=enc(knownWells[k])+(wellType[k]<<12);for(int i=4;i<20;i++){int old=rc.readSharedArray(i);if(old==val)break;if(old==0){write(i,val);break;}}
   }
   for(int id=1;id<36;id++)if(knownIslands[id]!=null){int old=rc.readSharedArray(19+id);if(islandSeen[id]==rc.getRoundNum()||old==0)write(19+id,enc(knownIslands[id])+(islandTeam[id]<<12));}
  }
 }
 static MapLocation nearestWell()throws GameActionException{
  int desired=mine==ResourceType.ADAMANTIUM?1:2;MapLocation best=null;int score=999999;
  for(int k=0;k<wellsCount;k++)if(wellType[k]==desired){int s=dist(rc.getLocation(),knownWells[k]);if(s<score){score=s;best=knownWells[k];}}
  for(int i=4;i<20;i++){int v=rc.readSharedArray(i);if((v>>12)==desired){MapLocation p=dec(v);int s=dist(rc.getLocation(),p);if(s<score){score=s;best=p;}}}
  return best;
 }
 static void headquarters()throws GameActionException{
  int round=rc.getRoundNum();
  boolean threatened=false;for(RobotInfo foe:rc.senseNearbyRobots(-1,enemy))if(foe.type==RobotType.LAUNCHER)threatened=true;
  boolean wantsAnchor=round>=90&&carriersBuilt>=6&&launchersBuilt>=6&&round-lastAnchorRound>=50&&!threatened&&rc.getNumAnchors(Anchor.STANDARD)==0;
  if(wantsAnchor&&rc.canBuildAnchor(Anchor.STANDARD)){rc.buildAnchor(Anchor.STANDARD);lastAnchorRound=round;}
  int reserve=wantsAnchor&&rc.getNumAnchors(Anchor.STANDARD)==0?80:0;
  for(int k=0;k<5&&rc.isActionReady();k++){
   RobotType type;
   if(carriersBuilt<4)type=RobotType.CARRIER;
   else if(rc.getResourceAmount(ResourceType.MANA)>=45+reserve)type=RobotType.LAUNCHER;
   else if(carriersBuilt<16&&rc.getResourceAmount(ResourceType.ADAMANTIUM)>=50+reserve)type=RobotType.CARRIER;
   else break;
   MapLocation target=type==RobotType.CARRIER?nearestWell():new MapLocation(width/2,height/2);
   if(target==null)target=new MapLocation(width/2,height/2);
   MapLocation best=null;int score=999999;
   for(MapLocation p:rc.getAllLocationsWithinRadiusSquared(rc.getLocation(),9))if(rc.canBuildRobot(type,p)){
    int s=dist(p,target)*8+random(5);if(s<score){score=s;best=p;}}
   if(best==null)break;rc.buildRobot(type,best);if(type==RobotType.CARRIER)carriersBuilt++;else launchersBuilt++;
  }
 }
 static void deposit()throws GameActionException{
  if(home==null)return;
  for(ResourceType t:new ResourceType[]{ResourceType.ADAMANTIUM,ResourceType.MANA,ResourceType.ELIXIR}){int n=rc.getResourceAmount(t);if(n>0&&rc.canTransferResource(home,t,n))rc.transferResource(home,t,n);}
 }
 static void carrier()throws GameActionException{
  MapLocation p=rc.getLocation();
  if(rc.getAnchor()!=null){anchorRun();return;}
  if(home!=null&&dist(p,home)<=2){deposit();if(rc.getWeight()==0&&rc.canTakeAnchor(home,Anchor.STANDARD)){rc.takeAnchor(home,Anchor.STANDARD);goal=null;anchorRun();return;}}
  RobotInfo threat=null;for(RobotInfo r:rc.senseNearbyRobots(-1,enemy))if(r.type==RobotType.LAUNCHER&&(threat==null||dist(p,r.location)<dist(p,threat.location)))threat=r;
  if(threat!=null&&dist(p,threat.location)<=16){if(rc.getWeight()>0&&rc.getHealth()<55&&rc.canAttack(threat.location))rc.attack(threat.location);flee(threat.location);return;}
  if(rc.getWeight()>=40){if(home!=null)moveTo(home);else explore();deposit();return;}
  well=nearestWell();
  if(well!=null){if(rc.canCollectResource(well,-1))rc.collectResource(well,-1);if(rc.getWeight()<40&&dist(rc.getLocation(),well)>2)moveTo(well);if(rc.canCollectResource(well,-1))rc.collectResource(well,-1);}
  else explore();
 }
 static void anchorRun()throws GameActionException{
  if(rc.canPlaceAnchor()){int id=rc.senseIsland(rc.getLocation());if(id>=0&&rc.senseTeamOccupyingIsland(id)==Team.NEUTRAL){rc.placeAnchor();if(id<36){islandTeam[id]=1;write(19+id,enc(rc.getLocation())+(1<<12));}goal=null;return;}}
  MapLocation best=null;int bestScore=999999;
  for(int id=1;id<36;id++){
   int v=rc.readSharedArray(19+id);MapLocation p=knownIslands[id]!=null?knownIslands[id]:dec(v);int t=knownIslands[id]!=null&&(islandSeen[id]==rc.getRoundNum()||v==0)?islandTeam[id]:(v>>12);
   if(p!=null&&t==0){int s=dist(rc.getLocation(),p);if(s<bestScore){bestScore=s;best=p;}}
  }
  if(best!=null)moveTo(best);else explore();
 }
 static RobotInfo attackBest()throws GameActionException{
  RobotInfo best=null;int score=-999999;
  for(RobotInfo r:rc.senseNearbyRobots(-1,enemy))if(r.type!=RobotType.HEADQUARTERS&&rc.canAttack(r.location)){
   int s=(r.type==RobotType.LAUNCHER?10000:0)-r.health*10-dist(rc.getLocation(),r.location);
   if(s>score){score=s;best=r;}}
  if(best!=null)rc.attack(best.location);return best;
 }
 static void launcher()throws GameActionException{
  MapLocation p=rc.getLocation();RobotInfo[] foes=rc.senseNearbyRobots(-1,enemy),friends=rc.senseNearbyRobots(-1,team);
  RobotInfo closest=null;int enemies=0,allies=1;
  for(RobotInfo r:friends)if(r.type==RobotType.LAUNCHER)allies++;
  for(RobotInfo r:foes)if(r.type!=RobotType.HEADQUARTERS){if(r.type==RobotType.LAUNCHER)enemies++;if(closest==null||dist(p,r.location)<dist(p,closest.location))closest=r;}
  RobotInfo shot=attackBest();
  if(closest!=null){
   if(enemies>allies||(rc.getHealth()<65&&enemies>0)||(shot!=null&&closest.type==RobotType.LAUNCHER&&dist(p,closest.location)<=9))flee(closest.location);
   else if(dist(p,closest.location)>9)moveTo(closest.location);
  }else{
   if(rc.getRoundNum()<70)moveTo(new MapLocation(width/2,height/2));
   else{if(goal==null||dist(p,goal)<9)goal=new MapLocation(random(width),random(height));moveTo(goal);}
  }
  attackBest();
 }
 static void flee(MapLocation threat)throws GameActionException{
  MapLocation p=rc.getLocation();Direction best=null;int score=dist(p,threat);
  for(Direction d:dirs)if(rc.canMove(d)){int s=dist(p.add(d),threat);if(s>score){score=s;best=d;}}
  if(best!=null)rc.move(best);
 }
 static void explore()throws GameActionException{
  if(goal==null||dist(rc.getLocation(),goal)<5||age%35==0)goal=new MapLocation(random(width),random(height));moveTo(goal);
 }
 static boolean safeMove(Direction d,RobotInfo[] foes)throws GameActionException{
  if(!rc.canMove(d))return false;MapLocation q=rc.getLocation().add(d);
  MapLocation end=q.add(rc.senseMapInfo(q).getCurrentDirection());
  for(RobotInfo r:foes)if(r.type==RobotType.HEADQUARTERS&&dist(end,r.location)<=9)return false;
  return true;
 }
 static void moveTo(MapLocation target)throws GameActionException{
  if(navTarget==null||!navTarget.equals(target)){navTarget=target;navBest=999999;navStall=0;wallMode=false;}
  RobotInfo[] foes=rc.senseNearbyRobots(-1,enemy);
  for(int step=0;step<2&&rc.isMovementReady();step++){
   MapLocation p=rc.getLocation();int nowDist=dist(p,target);if(nowDist<=2)return;
   if(nowDist<navBest){navBest=nowDist;navStall=0;}else navStall++;
   Direction direct=p.directionTo(target);
   if(!wallMode&&navStall>=20){wallMode=true;wallDir=direct;wallHit=nowDist;wallSteps=0;}
   if(wallMode&&nowDist<wallHit&&safeMove(direct,foes)){wallMode=false;navStall=0;}
   Direction best=null;
   if(wallMode){
    Direction d=wallDir;boolean left=(rc.getID()%2==0);
    for(int i=0;i<8;i++){if(safeMove(d,foes)){best=d;break;}d=left?d.rotateLeft():d.rotateRight();}
    if(best!=null){wallDir=left?best.rotateRight().rotateRight():best.rotateLeft().rotateLeft();}
    if(++wallSteps>90){wallMode=false;navStall=0;navBest=999999;}
   }else{
    int bestScore=999999;
    for(Direction d:dirs)if(safeMove(d,foes)){
     MapLocation q=p.add(d);MapInfo info=rc.senseMapInfo(q);MapLocation end=q.add(info.getCurrentDirection());if(!rc.onTheMap(end))end=q;
     int ago=rc.getRoundNum()-visited[end.x+60*end.y];
     int score=dist(end,target)*4+(ago<8?(8-ago)*12:0)+(info.hasCloud()?3:0)+random(3);
     if(score<bestScore){bestScore=score;best=d;}
    }
   }
   if(best==null)return;rc.move(best);MapLocation n=rc.getLocation();visited[n.x+60*n.y]=rc.getRoundNum();if(dist(n,target)<=2)return;
  }
 }
}
