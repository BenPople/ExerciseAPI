import UIKit

class ViewController: UIViewController {
    @IBOutlet weak var usernameTextField: UITextField!
    @IBOutlet weak var detailsTextView: UITextView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        detailsTextView.isEditable = false
    }
    
    @IBAction func getUserDetailsButtonPressed(_ sender: UIButton) {
        guard let username = usernameTextField.text else {
            return
        }
        
        fetchUserIdByUsername(username: username) { userId in
            self.fetchUserDetailsById(userId: userId) { userDetails in
                DispatchQueue.main.async {
                    self.displayUserDetails(userDetails)
                }
            }
        }
    }
    
    func fetchUserIdByUsername(username: String, completion: @escaping (Int?) -> Void) {
        let urlString = "http://localhost:5000/api/users/get/id/byusername?username=\(username)"
        guard let url = URL(string: urlString) else {
            return
        }
        
        URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                print("Error: \(error.localizedDescription)")
                completion(nil)
                return
            }
            
            guard let httpResponse = response as? HTTPURLResponse,
                  (200..<300).contains(httpResponse.statusCode) else {
                      print("Error: Invalid response")
                      completion(nil)
                      return
                  }
            
            guard let data = data else {
                print("Error: No data received")
                completion(nil)
                return
            }
            
            do {
                let json = try JSONSerialization.jsonObject(with: data, options: [])
                if let dict = json as? [String: Any],
                   let userId = dict["user_id"] as? Int {
                    completion(userId)
                } else {
                    completion(nil)
                }
            } catch {
                print("Error: \(error.localizedDescription)")
                completion(nil)
            }
        }.resume()
    }
    
    func fetchUserDetailsById(userId: Int, completion: @escaping ([String: Any]?) -> Void) {
        let urlString = "http://localhost:5000/api/users/get/byid?id=\(userId)"
        guard let url = URL(string: urlString) else {
            return
        }
        
        URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                print("Error: \(error.localizedDescription)")
                completion(nil)
                return
            }
            
            guard let httpResponse = response as? HTTPURLResponse,
                  (200..<300).contains(httpResponse.statusCode) else {
                      print("Error: Invalid response")
                      completion(nil)
                      return
                  }
            
            guard let data = data else {
                print("Error: No data received")
                completion(nil)
                return
            }
            
            do {
                let userDetails = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any]
                completion(userDetails)
            } catch {
                print("Error: \(error.localizedDescription)")
                completion(nil)
            }
        }.resume()
    }
    
    func displayUserDetails(_ userDetails: [String: Any]?) {
        guard let userDetails = userDetails,
              let id = userDetails["id"] as? Int,
              let name = userDetails["name"] as? String,
              let email = userDetails["email"] as? String else {
            detailsTextView.text = "Error: Failed to fetch user details"
            return
        }
        
        let userText = "User ID: \(id)\nName: \(name)\nEmail: \(email)"
        detailsTextView.text = userText
