import UIKit

class ViewController: UIViewController {
    @IBOutlet weak var usernameTextField: UITextField!
    @IBOutlet weak var passwordTextField: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    
    @IBAction func loginButtonPressed(_ sender: UIButton) {
        guard let username = usernameTextField.text,
              let password = passwordTextField.text else {
            return
        }
        
        let parameters = ["username": username, "password": password]
        
        guard let url = URL(string: "http://localhost:5000/api/users/login") else {
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        do {
            let jsonData = try JSONSerialization.data(withJSONObject: parameters, options: [])
            request.httpBody = jsonData
        } catch {
            print("Error: \(error.localizedDescription)")
            return
        }
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error: \(error.localizedDescription)")
                return
            }
            
            guard let httpResponse = response as? HTTPURLResponse,
                  (200..<300).contains(httpResponse.statusCode) else {
                      print("Error: Invalid response")
                      return
                  }
            
            guard let data = data else {
                print("Error: No data received")
                return
            }
            
            do {
                let userData = try JSONDecoder().decode([User].self, from: data)
                if userData.count > 0 {
                    UserData.shared.currentUser = userData
                    print("User logged in successfully")
                } else {
                    print("Invalid username or password")
                }
            } catch {
                print("Error: \(error.localizedDescription)")
            }
        }.resume()
    }
}

struct User: Codable {
    let id: Int
    let name: String
    let email: String
    let username: String
    let password: String
}
