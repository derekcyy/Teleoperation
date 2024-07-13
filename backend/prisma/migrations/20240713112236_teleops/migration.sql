/*
  Warnings:

  - You are about to drop the column `scan` on the `Lidar` table. All the data in the column will be lost.
  - You are about to drop the column `createdAt` on the `TurtleBot` table. All the data in the column will be lost.
  - You are about to drop the `Map` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `Waypoint` table. If the table is not empty, all the data it contains will be lost.
  - Changed the type of `image` on the `Camera` table. No cast exists, the column would be dropped and recreated, which cannot be done if there is data, since the column is required.

*/
-- DropForeignKey
ALTER TABLE "Map" DROP CONSTRAINT "Map_turtleBotId_fkey";

-- DropForeignKey
ALTER TABLE "Waypoint" DROP CONSTRAINT "Waypoint_turtleBotId_fkey";

-- DropIndex
DROP INDEX "TurtleBot_name_key";

-- AlterTable
ALTER TABLE "Camera" DROP COLUMN "image",
ADD COLUMN     "image" BYTEA NOT NULL;

-- AlterTable
ALTER TABLE "Lidar" DROP COLUMN "scan",
ADD COLUMN     "ranges" DOUBLE PRECISION[];

-- AlterTable
ALTER TABLE "TurtleBot" DROP COLUMN "createdAt";

-- DropTable
DROP TABLE "Map";

-- DropTable
DROP TABLE "Waypoint";
