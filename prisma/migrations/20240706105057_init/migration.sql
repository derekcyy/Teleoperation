-- CreateTable
CREATE TABLE "TurtleBot" (
    "id" SERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "TurtleBot_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Telemetry" (
    "id" SERIAL NOT NULL,
    "turtleBotId" INTEGER NOT NULL,
    "timestamp" TIMESTAMP(3) NOT NULL,
    "x" DOUBLE PRECISION NOT NULL,
    "y" DOUBLE PRECISION NOT NULL,
    "heading" DOUBLE PRECISION NOT NULL,

    CONSTRAINT "Telemetry_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Battery" (
    "id" SERIAL NOT NULL,
    "turtleBotId" INTEGER NOT NULL,
    "timestamp" TIMESTAMP(3) NOT NULL,
    "voltage" DOUBLE PRECISION NOT NULL,
    "current" DOUBLE PRECISION NOT NULL,
    "percentage" DOUBLE PRECISION NOT NULL,

    CONSTRAINT "Battery_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Camera" (
    "id" SERIAL NOT NULL,
    "turtleBotId" INTEGER NOT NULL,
    "timestamp" TIMESTAMP(3) NOT NULL,
    "image" TEXT NOT NULL,

    CONSTRAINT "Camera_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Lidar" (
    "id" SERIAL NOT NULL,
    "turtleBotId" INTEGER NOT NULL,
    "timestamp" TIMESTAMP(3) NOT NULL,
    "scan" TEXT NOT NULL,

    CONSTRAINT "Lidar_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Waypoint" (
    "id" SERIAL NOT NULL,
    "turtleBotId" INTEGER NOT NULL,
    "timestamp" TIMESTAMP(3) NOT NULL,
    "x" DOUBLE PRECISION NOT NULL,
    "y" DOUBLE PRECISION NOT NULL,
    "theta" DOUBLE PRECISION NOT NULL,

    CONSTRAINT "Waypoint_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Map" (
    "id" SERIAL NOT NULL,
    "turtleBotId" INTEGER NOT NULL,
    "timestamp" TIMESTAMP(3) NOT NULL,
    "data" TEXT NOT NULL,

    CONSTRAINT "Map_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "TurtleBot_name_key" ON "TurtleBot"("name");

-- AddForeignKey
ALTER TABLE "Telemetry" ADD CONSTRAINT "Telemetry_turtleBotId_fkey" FOREIGN KEY ("turtleBotId") REFERENCES "TurtleBot"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Battery" ADD CONSTRAINT "Battery_turtleBotId_fkey" FOREIGN KEY ("turtleBotId") REFERENCES "TurtleBot"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Camera" ADD CONSTRAINT "Camera_turtleBotId_fkey" FOREIGN KEY ("turtleBotId") REFERENCES "TurtleBot"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Lidar" ADD CONSTRAINT "Lidar_turtleBotId_fkey" FOREIGN KEY ("turtleBotId") REFERENCES "TurtleBot"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Waypoint" ADD CONSTRAINT "Waypoint_turtleBotId_fkey" FOREIGN KEY ("turtleBotId") REFERENCES "TurtleBot"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Map" ADD CONSTRAINT "Map_turtleBotId_fkey" FOREIGN KEY ("turtleBotId") REFERENCES "TurtleBot"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
