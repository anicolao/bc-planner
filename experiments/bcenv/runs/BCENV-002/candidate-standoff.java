package mybot;

import battlecode.common.*;

/** Independent local diagnostic entrant. No opponent implementation is used. */
public strictfp class RobotPlayer {
    static final Direction[] DIRS = {Direction.NORTH,Direction.NORTHEAST,Direction.EAST,Direction.SOUTHEAST,Direction.SOUTH,Direction.SOUTHWEST,Direction.WEST,Direction.NORTHWEST};
    static RobotController rc;
    static MapLocation home, well, waypoint;
    static int homeIndex=-1, carriers=0, age=0, exploration=0;
    static MapLocation[] recent=new MapLocation[12];
    static int recentIndex=0;
    static ResourceType preference;

    public static void run(RobotController controller) {
        rc=controller;
        preference=rc.getID()%3==0?ResourceType.ADAMANTIUM:ResourceType.MANA;
        while(true) {
            try {
                age++;
                if(rc.getType()==RobotType.HEADQUARTERS) headquarters();
                else {
                    findHome();
                    observe();
                    if(rc.getType()==RobotType.CARRIER) carrier();
                    else if(rc.getType()==RobotType.LAUNCHER) launcher();
                }
            } catch(Exception e) {
                System.out.println("candidate exception round="+rc.getRoundNum()+" id="+rc.getID()+" "+e.toString());
            } finally { Clock.yield(); }
        }
    }
    static int encode(MapLocation p) {return 1+p.x+rc.getMapWidth()*p.y;}
    static MapLocation decode(int v) {v=(v%4096)-1;return new MapLocation(v%rc.getMapWidth(),v/rc.getMapWidth());}
    static void write(int slot,int value) throws GameActionException {
        if(rc.canWriteSharedArray(slot,value))rc.writeSharedArray(slot,value);
    }
    static void findHome() throws GameActionException {
        if(home!=null)return;
        int best=100000;
        for(int i=0;i<4;i++) {
            int value=rc.readSharedArray(i);
            if(value>0){MapLocation p=decode(value);int d=rc.getLocation().distanceSquaredTo(p);if(d<best){best=d;home=p;homeIndex=i;}}
        }
        if(home==null) for(RobotInfo r:rc.senseNearbyRobots(-1,rc.getTeam())) if(r.type==RobotType.HEADQUARTERS){home=r.location;homeIndex=0;break;}
    }
    static void observe() throws GameActionException {
        for(WellInfo w:rc.senseNearbyWells()) {
            if(w.getResourceType()==preference && (well==null || home!=null && w.getMapLocation().distanceSquaredTo(home)<well.distanceSquaredTo(home)))well=w.getMapLocation();
            if(homeIndex>=0 && w.getResourceType()!=ResourceType.ELIXIR) {
                int slot=(w.getResourceType()==ResourceType.ADAMANTIUM?8:12)+homeIndex;
                int old=rc.readSharedArray(slot);
                if(old==0 || home!=null && w.getMapLocation().distanceSquaredTo(home)<decode(old).distanceSquaredTo(home))write(slot,encode(w.getMapLocation()));
            }
        }
        for(int id:rc.senseNearbyIslands()) {
            MapLocation[] locs=rc.senseNearbyIslandLocations(id);
            if(locs.length>0) {
                Team t=rc.senseTeamOccupyingIsland(id);
                int flag=t==Team.NEUTRAL?0:(t==rc.getTeam()?4096:8192);
                write(20+id,encode(locs[0])+flag);
            }
        }
    }
    static void headquarters() throws GameActionException {
        if(homeIndex<0) {
            for(int i=0;i<4;i++)if(rc.readSharedArray(i)==0){homeIndex=i;home=rc.getLocation();write(i,encode(home));break;}
        }
        observe();
        for(int j=0;j<5 && rc.isActionReady();j++) {
            boolean reserve=rc.getRoundNum()>120 && carriers>=4 && rc.getNumAnchors(Anchor.STANDARD)==0;
            if(reserve && rc.canBuildAnchor(Anchor.STANDARD)){rc.buildAnchor(Anchor.STANDARD);continue;}
            RobotType type;
            if(carriers<4)type=RobotType.CARRIER;
            else if(carriers<8 && rc.getResourceAmount(ResourceType.ADAMANTIUM)>150)type=RobotType.CARRIER;
            else if(!reserve || rc.getResourceAmount(ResourceType.MANA)>=160)type=RobotType.LAUNCHER;
            else break;
            MapLocation best=null;int score=100000;
            MapLocation goal=type==RobotType.CARRIER?well:new MapLocation(rc.getMapWidth()/2,rc.getMapHeight()/2);
            if(goal==null)goal=new MapLocation(rc.getMapWidth()/2,rc.getMapHeight()/2);
            for(MapLocation p:rc.getAllLocationsWithinRadiusSquared(rc.getLocation(),9))if(rc.canBuildRobot(type,p)) {
                int s=p.distanceSquaredTo(goal);if(s<score){score=s;best=p;}
            }
            if(best==null)break;
            rc.buildRobot(type,best);if(type==RobotType.CARRIER)carriers++;
        }
    }
    static void carrier() throws GameActionException {
        if(rc.getAnchor()!=null) { deliverAnchor(); return; }
        int weight=rc.getWeight();
        if(home!=null && (weight>=40 || weight>0 && rc.getLocation().distanceSquaredTo(home)<=2)) {
            for(ResourceType r:ResourceType.values()) {
                int amount=rc.getResourceAmount(r);
                if(amount>0 && rc.canTransferResource(home,r,amount))rc.transferResource(home,r,amount);
            }
            if(rc.getWeight()>0){moveToward(home);return;}
        }
        if(home!=null && rc.getWeight()==0 && rc.canTakeAnchor(home,Anchor.STANDARD)) {
            rc.takeAnchor(home,Anchor.STANDARD);deliverAnchor();return;
        }
        if(well==null && homeIndex>=0) {
            int v=rc.readSharedArray((preference==ResourceType.ADAMANTIUM?8:12)+homeIndex);
            if(v>0)well=decode(v);
        }
        if(well!=null) {
            if(rc.canCollectResource(well,-1))rc.collectResource(well,-1);
            if(rc.getWeight()>=40 && home!=null)moveToward(home);
            else if(rc.getLocation().distanceSquaredTo(well)>2)moveToward(well);
        } else explore();
    }
    static void deliverAnchor() throws GameActionException {
        MapLocation goal=null;int best=100000;
        for(int id:rc.senseNearbyIslands()) if(rc.senseTeamOccupyingIsland(id)==Team.NEUTRAL) {
            for(MapLocation p:rc.senseNearbyIslandLocations(id)) {
                int d=rc.getLocation().distanceSquaredTo(p);if(d<best){best=d;goal=p;}
            }
        }
        if(goal==null)for(int i=21;i<=55;i++) {
            int v=rc.readSharedArray(i);
            if(v>0 && v<4096) {
                MapLocation p=decode(v);
                if(rc.canSenseLocation(p)) {
                    int id=rc.senseIsland(p);
                    if(id<1 || rc.senseTeamOccupyingIsland(id)!=Team.NEUTRAL)continue;
                }
                int d=rc.getLocation().distanceSquaredTo(p);if(d<best){best=d;goal=p;}
            }
        }
        int island=rc.senseIsland(rc.getLocation());
        if(island>0 && rc.senseTeamOccupyingIsland(island)==Team.NEUTRAL && rc.canPlaceAnchor()){rc.placeAnchor();return;}
        if(goal!=null)moveToward(goal);else explore();
        island=rc.senseIsland(rc.getLocation());
        if(island>0 && rc.senseTeamOccupyingIsland(island)==Team.NEUTRAL && rc.canPlaceAnchor())rc.placeAnchor();
    }
    static RobotInfo attackTarget() throws GameActionException {
        RobotInfo target=null;int best=100000;
        for(RobotInfo e:rc.senseNearbyRobots(-1,rc.getTeam().opponent())) {
            if(e.type==RobotType.HEADQUARTERS || !rc.canAttack(e.location))continue;
            int score=e.health+(e.type==RobotType.LAUNCHER?0:1000);
            if(score<best){best=score;target=e;}
        }
        if(target!=null)rc.attack(target.location);
        return target;
    }
    static void launcher() throws GameActionException {
        attackTarget();
        RobotInfo closest=null;int best=100000;
        for(RobotInfo e:rc.senseNearbyRobots(-1,rc.getTeam().opponent()))if(e.type!=RobotType.HEADQUARTERS) {
            int d=rc.getLocation().distanceSquaredTo(e.location);int score=d+(e.type==RobotType.LAUNCHER?0:100);
            if(score<best){best=score;closest=e;}
        }
        if(closest!=null) {
            if(closest.type==RobotType.LAUNCHER && rc.getLocation().distanceSquaredTo(closest.location)<=16)standoff(closest.location);
            else moveToward(closest.location);
        }
        else {
            MapLocation center=new MapLocation(rc.getMapWidth()/2,rc.getMapHeight()/2);
            if(age<40 || home==null)moveToward(center);
            else {
                int phase=(age/60+rc.getID())%3;
                MapLocation goal=new MapLocation(phase==0?home.x:rc.getMapWidth()-1-home.x,phase==1?home.y:rc.getMapHeight()-1-home.y);
                moveToward(goal);
            }
        }
        attackTarget();
    }
    // Experiment001: only engaged-launcher movement is changed.
    static void standoff(MapLocation enemy) throws GameActionException {
        if(!rc.isMovementReady())return;
        Direction choice=null;
        int best=Math.abs(rc.getLocation().distanceSquaredTo(enemy)-13)*4;
        RobotInfo[] enemies=rc.senseNearbyRobots(-1,rc.getTeam().opponent());
        for(Direction d:DIRS)if(rc.canMove(d)) {
            MapLocation p=rc.getLocation().add(d);
            int score=Math.abs(p.distanceSquaredTo(enemy)-13)*4;
            for(RobotInfo e:enemies)if(e.type==RobotType.HEADQUARTERS && p.distanceSquaredTo(e.location)<=9)score+=1000;
            if(score<best){best=score;choice=d;}
        }
        if(choice!=null)rc.move(choice);
    }
    static void explore() throws GameActionException {
        if(waypoint==null || rc.getLocation().distanceSquaredTo(waypoint)<=4 || age%40==0) {
            exploration++;
            int seed=rc.getID()*31+exploration*7919;
            int x=(seed&0x7fffffff)%rc.getMapWidth();
            int y=((seed*73)&0x7fffffff)%rc.getMapHeight();
            waypoint=new MapLocation(x,y);
        }
        moveToward(waypoint);
    }
    static void moveToward(MapLocation target) throws GameActionException {
        if(target==null || !rc.isMovementReady())return;
        Direction bestDir=null;int best=100000;
        RobotInfo[] enemies=rc.getType()==RobotType.LAUNCHER?rc.senseNearbyRobots(-1,rc.getTeam().opponent()):new RobotInfo[0];
        int offset=(rc.getID()+age)%8;
        for(int i=0;i<8;i++) {
            Direction d=DIRS[(i+offset)%8];if(!rc.canMove(d))continue;
            MapLocation p=rc.getLocation().add(d);int score=p.distanceSquaredTo(target)*4;
            for(MapLocation old:recent)if(p.equals(old))score+=12;
            for(RobotInfo e:enemies)if(e.type==RobotType.HEADQUARTERS && p.distanceSquaredTo(e.location)<=9)score+=1000;
            if(score<best){best=score;bestDir=d;}
        }
        if(bestDir!=null) {
            recent[recentIndex]=rc.getLocation();recentIndex=(recentIndex+1)%recent.length;
            rc.move(bestDir);
        }
    }
}
