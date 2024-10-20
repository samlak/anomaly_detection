import time
import random
import matplotlib.pyplot as plt
import math 

# This algorithm calculates a moving average of recent data points within a specified window. 
# A dynamic threshold is then calculated based on the standard deviation within that window.  
# An anomaly is flagged if the current data point exceeds this threshold. 
# This approach is effective because the dynamic threshold adapts to changing data patterns 
# and data spread, making it more robust than a fixed threshold. 
# It's computationally efficient and suitable for real-time detection.  
# It handles concept drift reasonably well due to the moving window's focus on recent data. 

# Anomaly Detection 
def detect_anomaly(data_point, window, threshold_factor):
    # Minimum window size before anomaly detection 
    if len(window) < 5: 
        return False

    avg = sum(window) / len(window) 
    std_dev = math.sqrt(sum([(x - avg)**2 for x in window]) / len(window)) # Standard deviation
    threshold = avg + threshold_factor * std_dev
    
    return data_point > threshold


# Data Stream Simulation 
def simulate_data_stream(length):
    for _ in range(length):
        base = 10  # Baseline value
        seasonal_variation = 5 * random.random()  # Add some random noise
        value = base + seasonal_variation  

        # Introduce occasional anomalies
        if random.random() < 0.02: # 2% chance of anomaly
            value += random.uniform(10, 20) 

        time.sleep(0.02)  # Slower for easier visualization
        yield value


# Visualization (using matplotlib)
plt.ion()
fig, ax = plt.subplots()
x, y = [], []
line, = ax.plot(x, y)


# Main Execution
if __name__ == "__main__":
    window = []
    window_size = 20
    threshold_factor = 2.5
    simulation_length = 500

    data_stream = simulate_data_stream(simulation_length)

    for i, data_point in enumerate(data_stream):
        window.append(data_point)
        if len(window) > window_size:
            window.pop(0)

        is_anomaly = detect_anomaly(data_point, window, threshold_factor)

        x.append(i)
        y.append(data_point)
        line.set_data(x, y)
        ax.relim()
        ax.autoscale_view()

        if is_anomaly:
            ax.plot(i, data_point, 'ro')  # Red dots for anomalies
            print(f"Anomaly detected at {i}: {data_point}")

        fig.canvas.draw()
        fig.canvas.flush_events()

    plt.ioff()
    plt.show()