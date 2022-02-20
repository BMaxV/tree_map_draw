from gamedevstuff import Vorrewrite
from vector import vector
from geom import geom
import random
import math

#I just realized the other way to draw this would be the force directed method I
#had.
#I can probably do something to move points in particular directions.

def box_test():
    rec=geom.rectangle(d_vec=vector.Vector(4,4,0))
    out_objects=[rec]
    view_box_d=geom.make_view_box_d(out_objects)
    output_l=[]
    for x in out_objects:
        output_l.append(x.as_svg())
        
    geom.main_svg(output_l,"box_test.svg",view_box_d=view_box_d)

def main():
    
    #this is using a voronoi thing. not sure if this is the final thing.
    #output looks "eh" but does produce a result.
    
    points=[]
    rec=geom.rectangle(d_vec=vector.Vector(4,4,0))
    print(rec.points)
    for x in range(100):
        points.append(4*vector.Vector(random.random(),random.random(),0))
    
    verts,faces,neighbors,centers,points=Vorrewrite.vor(points,3,rec.points)
    
    print(centers)
    
    #middle upper side
    tree_start_point=vector.Vector(2,2,0)
    max_d=float("inf")
    counter=0
    for c in centers:
        #print(c)
        C=vector.Vector(*c)
        d=(C-tree_start_point).magnitude()
        if d < max_d:
            max_d=d
            max_d_i=counter
        counter+=1
    visited=[]
    next_row=[max_d_i]
    next_row_eh=[]
    out_objects=[rec]
    used_neighbors=[max_d_i]
    #there should be some additional map of how many outgoing connections
    #I need, assume I will use half of the available neighbors
    max_level=3
    current_level=0
    while True:
        print("yo",next_row)
        for index in next_row:
            out_objects.append(geom.circle(local_position=centers[index],radius=0.1))
            #next_row_eh+=neighbors[index]
            available_neighbors=list(neighbors[index])
            #print(available_neighbors)
            #print(index)
            
            #removed those already used up
            #ideally, I should move them up to maximize space
            for x in used_neighbors:
                if x in available_neighbors:
                    available_neighbors.remove(x)
            
            n_neighbors=len(available_neighbors)
            use_neighbors=int(max(round(n_neighbors/2,0),1))
            #sprint(use_neighbors)
            use_these=random.sample(available_neighbors,use_neighbors)
            print("using these",use_these)
            next_row_eh+=use_these
            used_neighbors+=use_these
            for x in use_these:
                print("drawing lines",index,x)
                out_objects.append(geom.Line.from_two_points(centers[index],centers[x]))
                
        next_row=next_row_eh
        next_row=list(set(next_row))
        current_level+=1
        if current_level==max_level:
            break
    
    view_box_d=geom.make_view_box_d(out_objects)
    output_l=[]
    for x in out_objects:
        output_l.append(x.as_svg())
        
    geom.main_svg(output_l,"test_out.svg",view_box_d=view_box_d)
            
            


def recursive_ginko_draw(data,from_layer,layer_number):
    p0=vector.Vector(2,0,0)
    diff=vector.Vector(0,-0.6+0.1*layer_number,0)
    #print(layer_number)
    print(from_layer)
    #input()
    # I want the points to be spread over an arc of 120° downwards.
    # I want the points in this layer to be in the middle relative to
    # the next layer they link to.
    
    circle_center=p0+layer_number*diff
    fac=1
    circle_radius=layer_number*fac
    next_layer=[]
    next_layer_length_sum=0
    for x in from_layer:
        if x in data:
            next_layer_length_sum+=len(data[x])
            next_layer+=data[x]
    
    if next_layer_length_sum==0:
        next_layer_length_sum=len(from_layer)
    
    relative_size_dict={}
    for x in from_layer:
        if x in data:
            
            relative_size_dict[x]=len(data[x])/next_layer_length_sum
        else:
            relative_size_dict[x]=1/next_layer_length_sum
    current_angle=210
    more_size=120
    #additional
    angles={}
    for x in relative_size_dict:
        this_full_size=more_size*relative_size_dict[x]
        print("tfs",this_full_size)
        angles[x]=current_angle+this_full_size/2
        print(angles[x])
        current_angle+=this_full_size
        
    #out_objects=[]
    positions={}
    offset_vector=vector.Vector(0.9+0.2*layer_number,0,0)
    axis=vector.Vector(0,0,1)
    for x in from_layer:
        if x in angles:
            this_angle=angles[x]
            #center + rotated offset
            print(this_angle)
            M=vector.RotationMatrix(this_angle/360*math.pi*2,axis)
            print(offset_vector)
            this_pos=circle_center+M*offset_vector
            positions[x]=this_pos
    
    print(positions)
            
    if from_layer!=[]:
        positions.update(recursive_ginko_draw(data,next_layer,layer_number+1))
    
    return positions

def top_down_ginko_like():
    layers={1:[2,3],2:[4,5,6],3:[7,8],4:[9],5:[10],6:[11]}#,7:[12]}#,8:[13]}
    data=layers
    #hmmm recursive drawing would be best.
    out_objects=[]
    current_layer=0
    from_layer=[1]
    object_positions=recursive_ginko_draw(data,from_layer,0)
    
    for x in layers:
        for xi in layers[x]:
            pos1,pos2=object_positions[x],object_positions[xi]
            out_objects.append(geom.circle(pos1,radius=0.1))
            if xi not in layers:
                out_objects.append(geom.circle(pos2,radius=0.1))
            out_objects.append(geom.Line.from_two_points(pos1,pos2))
            
    view_box_d=geom.make_view_box_d(out_objects)
    final_l=[]
    for x in out_objects:
        final_l.append(x.as_svg())
    
    geom.main_svg(final_l,"ginko_tree.svg",view_box_d=view_box_d)

    
        
    
    
if __name__=="__main__":
    #main()
    #box_test()
    top_down_ginko_like()
   
