import UIKit

class ViewController: UIViewController {
    @IBOutlet weak var scrollView: UIScrollView!
    @IBOutlet weak var textView: UITextView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        textView.isEditable = false
        textView.textContainerInset = UIEdgeInsets(top: 20, left: 20, bottom: 20, right: 20)
        
        fetchAllUsers()
    }
    
    func fetchAllUsers() {
        let url = URL(string: "http://localhost:5000/api/users/get/all")!
        
        URLSession.shared.dataTask(with: url) { data, response, error in
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
                let usersData = try JSONDecoder().decode([User].self, from: data)
                DispatchQueue.main.async {
                    self.addTextForUsers(users: usersData)
                }
            } catch {
                print("Error: \(error.localizedDescription)")
            }
        }.resume()
    }
    
    func addTextForUsers(users: [User]) {
        var userText = ""
        for user in users {
            userText += "Name: \(user.name)\nEmail: \(user.email)\n\n"
        }
        
        textView.text = userText
        textView.sizeToFit()
        scrollView.contentSize = CGSize(width: scrollView.frame.size.width, height: textView.frame.size.height)
    }
}

struct User: Codable {
    let id: Int
    let name: String
    let email: String
}
