import ezdxf
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
from ezdxf.enums import TextEntityAlignment
from ezdxf import units
import numpy as np
import math

def generate_points_on_circle(num_points, radius):
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x = radius * np.cos(angles)
    y = radius * np.sin(angles)
    return x, y

def calc_point_distance(x1,y1,x2,y2):
    try:
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    except: 
        return float('NaN')
    return distance

def plot_circle_with_points(num_points, radius,text_distance):
    x, y = generate_points_on_circle(num_points, radius)

    plt.figure('plot_circle_with_points')
    #plt.subplot(211)
    # Plot Kreis
    circle = plt.Circle((0, 0), radius, edgecolor='b', facecolor='none')
    plt.gca().add_patch(circle)

    # Plot Punkte
    #plt.scatter(x, y, color='red', label='Points on Circle')

    #plt.subplot(212)
    #Plot Font
    plt.scatter(x, y, color='red', label='Points on Circle')
    
    i=1
    for xi,yi in zip(x,y):
        angle = math.atan2(yi,xi)
        text_x = (radius + text_distance) * math.cos(angle)
        text_y = (radius + text_distance) * math.sin(angle)
        plt.annotate(str(i+1),(text_x,text_y))
        i +=1
    #plt.text(x,y,'Beispiel')

    # Punkte abstand
    distance = math.sqrt((x[1] - x[0])**2 + (y[1] - y[0])**2)

    # Figure Settings
    plt.axis('equal')
    plt.xlabel('X-Achse')
    plt.ylabel('Y-Achse')
    plt.title('Number of nails: '+ str(num_points) + '\n'+'Distance between Nails: '+ str(round(calc_point_distance(x[0],y[0],x[1],y[1]))))
    plt.legend()
    plt.grid(True)
    plt.show()
    return x,y

def show_dxf_live(filename):
    # DXF-Datei lesen
    doc = ezdxf.readfile(filename + '_points.dxf')
    doc2 = ezdxf.readfile(filename + '_Font.dxf')

        # Matplotlib-Figur erstellen
    #plt.figure('show_dxf_live')
    fig, ax = plt.subplots()
    #plt.get_current_fig_manager().canvas.set_window_title('show_dxf_live')
    ax.set_aspect('equal', 'box')
    ax.axis('equal')

    # DXF-Elemente durchgehen und in Matplotlib-Figur zeichnen
    for entity in doc.modelspace().query('*'):
        if entity.dxftype() == 'LINE':
            line = Line2D([entity.dxf.start.x, entity.dxf.end.x], [entity.dxf.start.y, entity.dxf.end.y])
            plt.gca().add_line(line)
        elif entity.dxftype() == 'CIRCLE':
            circle = Circle((entity.dxf.center.x, entity.dxf.center.y), entity.dxf.radius)
            plt.scatter(x, y, color='red')
            #plt.gca().add_patch(circle)
            #ax.add_patch(circle)

    for entity in doc2.modelspace().query('*'):
        if entity.dxftype() == 'TEXT':
            #font = plt.text(entity.dxf.center.x, entity.dxf.center.y, entity.dxf.text)
            plt.annotate(entity.dxf.text,(entity.dxf.insert.x,entity.dxf.insert.y))
            #plt.gca().add_patch(font)

    # Einstellungen für bessere Darstellung
    plt.axis('equal')
    plt.xlabel('X-Achse')
    plt.ylabel('Y-Achse')
    #plt.title('Number of nails: '+ str(num_points) + '\n'+'Distance between Nails: '+ str(round(calc_point_distance(x[0],y[0],x[1],y[1]))))
    plt.legend()
    plt.grid(True)
    plt.get_current_fig_manager().set_window_title('show_dxf_live')
    plt.show()
            

    # Matplotlib-Fenster anzeigen
    ax.axis('equal')
    plt.show()

def create_dxf(filename,x,y,radius,text_distance):
    # create DXF-File 
    docPoints = ezdxf.new()
    docFont = ezdxf.new(setup=True)
    # Set Drawing Units to Millimeters
    docPoints.units = units.MM
    docFont.units = units.MM
    docFont.styles.add("Arial", font="Arial.ttf")
    # Modelspace hinzufügen
    mspPoints = docPoints.modelspace()
    mspFont = docFont.modelspace()

    # Text zum Modellbereich hinzufügen



    # Add Circle/points and index as text
    FontIndex = 1
    FontSize = 2
    for xi, yi in zip(x, y):
        radius_smallCircle =0.1
        angle = math.atan2(yi,xi)
        mspPoints.add_circle(center = (xi-radius_smallCircle,yi-radius_smallCircle),radius = radius_smallCircle) #Circle needed since laser tool cannot see dxf points with no radius
        text_content = str(FontIndex)
        # Calculate the Font position outside the circle
        text_distance = 5.2  # Adjust this value to control the distance from the circle
        text_x = (radius + text_distance) * math.cos(angle)
        text_y = (radius + text_distance) * math.sin(angle)
        insertion_point = (text_x, text_y)  # x, y
        text_height = 5.0
        mspFont.add_text(
            text=text_content,
            dxfattribs={
            #'insert': insertion_point,
            'height': text_height,
            'style' : 'Arial'
            }
        ).set_placement(insertion_point,(insertion_point[0]+FontSize,insertion_point[1]+FontSize),align=TextEntityAlignment.ALIGNED)
        FontIndex += 1
    



    # DXF-Datei speichern
    docPoints.saveas(filename + '_points.dxf')
    print(f"DXF-Datei '{filename}_points.dxf' erfolgreich erstellt.")
    docFont.saveas(filename + '_Font.dxf')
    print(f"DXF-Datei '{filename}_Font.dxf' erfolgreich erstellt.")

def convert_dxf_to_png(dxf_filename, png_filename):
    # Read the DXF file
    doc = ezdxf.readfile(dxf_filename)
    
    # Create a Matplotlib figure
    fig, ax = plt.subplots()

    # Plot the entities from the DXF file onto Matplotlib axes
    for entity in doc.modelspace().query('*'):
        if entity.dxftype() == 'LINE':
            line = plt.Line2D([entity.dxf.start.x, entity.dxf.end.x], [entity.dxf.start.y, entity.dxf.end.y])
            ax.add_line(line)
        elif entity.dxftype() == 'LWPOLYLINE':
            points = [(point.x, point.y) for point in entity.points()]
            line = plt.Polygon(points, closed=False, fill=None, edgecolor='black')
            ax.add_patch(line)
        elif entity.dxftype() == 'TEXT':
            plt.annotate(entity.dxf.text,(entity.dxf.insert.x,entity.dxf.insert.y))


    # Set equal aspect ratio for proper scaling
    ax.set_aspect('equal', 'box')
    
    # Save the Matplotlib figure as a PNG file
    plt.savefig(png_filename, bbox_inches='tight')
    print(f"PNG file '{png_filename}' successfully created.")

if __name__ == "__main__":
    dxf_filename = "beispiel"
    diameter = 300
    radius = diameter/2
    nails = 8
    text_distance = 5  # Adjust this value to control the distance of the nail index font from the circle
    x,y= plot_circle_with_points(nails,radius,text_distance)
    create_dxf(dxf_filename,x,y,radius,text_distance)
    show_dxf_live(dxf_filename)
    #convert_dxf_to_png(dxf_filename+'_Font.dxf',dxf_filename+'.png')







