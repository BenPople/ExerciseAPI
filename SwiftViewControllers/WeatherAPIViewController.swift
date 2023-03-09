import UIKit

class ViewController: UIViewController {
    
    // MARK: - Outlets
    
    @IBOutlet weak var townTextField: UITextField!
    @IBOutlet weak var temperatureLabel: UILabel!
    
    // MARK: - Actions
    
    @IBAction func getTemperatureButtonPressed(_ sender: UIButton) {
        guard let town = townTextField.text?.trimmingCharacters(in: .whitespacesAndNewlines), !town.isEmpty else {
            temperatureLabel.text = "Please enter a town name"
            return
        }
        
        let apiKey = "22f5311399014dd0a40e36405f7e4205"
        let urlString = "https://api.openweathermap.org/data/2.5/weather?q=\(town)&appid=\(apiKey)&units=metric"
        guard let url = URL(string: urlString) else {
            temperatureLabel.text = "Invalid URL"
            return
        }
        
        let task = URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                DispatchQueue.main.async {
                    self.temperatureLabel.text = "Error: \(error.localizedDescription)"
                }
                return
            }
            
            guard let httpResponse = response as? HTTPURLResponse, (200..<300).contains(httpResponse.statusCode) else {
                DispatchQueue.main.async {
                    self.temperatureLabel.text = "Invalid response"
                }
                return
            }
            
            guard let data = data else {
                DispatchQueue.main.async {
                    self.temperatureLabel.text = "No data received"
                }
                return
            }
            
            do {
                let decoder = JSONDecoder()
                decoder.keyDecodingStrategy = .convertFromSnakeCase
                let weatherData = try decoder.decode(WeatherData.self, from: data)
                DispatchQueue.main.async {
                    self.temperatureLabel.text = "\(weatherData.temp)°C"
                }
            } catch {
                DispatchQueue.main.async {
                    self.temperatureLabel.text = "Error: \(error.localizedDescription)"
                }
            }
        }
        
        task.resume()
    }
    
}

struct WeatherData: Codable {
    let temp: Double
}
