import numpy as np
from matplotlib import pyplot as plt
import random

#K-Means algorithm model

#functions formatting and handling creating points matrix
def SpawnPoints(num_points,cluster_centre,diameter):
    points=np.zeros((num_points,2))
    for i in range(num_points):
        point = np.random.random((1, 2))
        while True:
            temp=point-0.5
            distance=np.sum(np.multiply(temp,temp))
            if distance>0.5**2:
                point=np.random.random((1,2))
            else:
                points[i,:]=point*diameter+np.array(cluster_centre)
                break
    return points

def PointsToArray(num_points,cluster_centre,diameter):
    points = np.zeros((np.sum(num_points), 2))
    temp = 0
    for i in range(len(num_points)):
        points[temp:temp + num_points[i], :] = SpawnPoints(num_points[i], cluster_centre[i, :], diameter[i])
        temp += num_points[i]
    return points

#randomly spawning centroids somwehere between clusters, with ability to define custom spawn point(input should be m x 2)
def SpawnCentroids(cluster_centre,diameter,num_centroids,coordinates=None):
    if coordinates:
        return np.array(coordinates)
    else:
        centroids=np.zeros((num_centroids,2))
        xrange = [np.min(cluster_centre[:,0],0), np.max(cluster_centre[:,0],0)]
        yrange = [np.min(cluster_centre[:,1],0), np.max(cluster_centre[:,1],0)]
        radmax=np.max(diameter)/2
        for i in range(num_centroids):
            centroids[i, :] = [random.uniform(xrange[0]-radmax, xrange[1]+radmax),
                                 random.uniform(yrange[0]-radmax, yrange[1])+radmax]
    return centroids

def CalcClosest(points,centroids):
    distance=np.zeros((np.shape(points)[0],np.shape(centroids)[0]))
    for i in range(np.shape(centroids)[0]):
        dif=(points-centroids[i,:])
        distance[:,i]=np.sqrt(np.sum(np.multiply(dif,dif),1))
    closest_index=np.argmin(distance,1)
    return closest_index

class KMeans():
    def __init__(self,num_points,cluster_centre,diameter,num_centroids):
        self.points=PointsToArray(num_points,cluster_centre,diameter)
        self.centroids=SpawnCentroids(cluster_centre,diameter, num_centroids)

    def update(self):
        index=CalcClosest(self.points,self.centroids)
        avgdist=np.zeros((np.shape(self.centroids)[0],2))
        ind=np.zeros((np.shape(self.centroids)[0],1))
        for i in range(np.shape(self.points)[0]):
            for j in range(np.shape(self.centroids)[0]):
                if index[i]==j:
                    avgdist[j,:]+=self.points[i,:]
                    ind[j]+=1

        for i in range(np.shape(ind)[0]):
            if ind[i]!=0:
                self.centroids[i,:]=np.divide(avgdist[i,:],ind[i])

    def main(self):
        #0 added to change memory position
        prev=self.centroids+0
        plt.scatter(self.points[:, 0], self.points[:, 1], marker=',' , cmap='o')
        plt.scatter(prev[:, 0], prev[:, 1], marker='o')
        plt.show()
        while True:
            self.update()
            new=self.centroids
            if np.sum(prev)-np.sum(new)==0:
                plt.scatter(self.points[:, 0], self.points[:, 1], marker=',')
                plt.scatter(new[:, 0], new[:, 1], marker='o')
                plt.show()
                break
            else:
                plt.scatter(self.points[:, 0], self.points[:, 1], marker=',')
                plt.scatter(new[:, 0], new[:, 1], marker='o')
                plt.show()
            prev=new+0


#example parameters
num_points=[50,50,50,50]
cluster_centre=np.array([[10,0],[0,10],[-5,-5],[-10,15]])
diameter=[12,12,12,12]

model=KMeans(num_points,cluster_centre,diameter,4)

model.main()