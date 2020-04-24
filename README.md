![Supported Python versions](https://img.shields.io/badge/python-3.6-blue.svg?style=flat-square)
![License](https://img.shields.io/badge/license-GNU-green.svg?style=flat-square)

# **ATTPwn**

```
____  ______  ______  ____  __    __  ____  
/    ||      ||      ||    \|  |__|  ||    \
|  o  ||      ||      ||  o  )  |  |  ||  _  |
|     ||_|  |_||_|  |_||   _/|  |  |  ||  |  |
|  _  |  |  |    |  |  |  |  |  `  '  ||  |  |
|  |  |  |  |    |  |  |  |   \      / |  |  |
|__|__|  |__|    |__|  |__|    \_/\_/  |__|__|

```

ATTPwn is a computer security tool designed to emulate adversaries. The tool aims to bring emulation of a real threat into closer contact with implementations based on the techniques and tactics from the MITRE ATT&CK framework. The goal is to simulate how a threat works in an intrusion scenario, where the threat has been successfully deployed. It is focused on Microsoft Windows systems through the use of the Powershell command line. This enables the different techniques based on MITRE ATT&CK to be applied. ATTPwn is designed to allow the emulation of adversaries as for a Red Team exercise and to verify the effectiveness and efficiency of the organization's controls in the face of a real threat.  

# Prerequisities
To run *ATTPwn* it is mandatory to have PowerShell 3.0 or higher.
To run the *ATTPwn* you need python 3 or higher and some python libraries. You can install this with:
```[python]
pip install -r requirements.txt
```

**Note**: ATTPwn works in **python 3.X**. Make sure you run a pip relative to this version.
# Usage
```[python]
python app.py
```
Now, open your browser: http://localhost:5000

# Example videos

### *ATTPwn - All-in-One: Discovery + privilege escalation + credential dumping + lateral movement on W10*
[![ATTPwn - All-in-One: Discovery + privilege escalation + credential dumping + lateral movement on W10](https://img.youtube.com/vi/2Y3F5uxXXSM/0.jpg)](https://youtu.be/2Y3F5uxXXSM)
### *ATTPwn - All-in-One: Discovery + privilege escalation + credential dumping + lateral movement on W7*
[![ATTPwn - All-in-One: Discovery + privilege escalation + credential dumping + lateral movement on W7](https://img.youtube.com/vi/Dge8Pquw4Bw/0.jpg)](https://youtu.be/Dge8Pquw4Bw)
### *ATTPwn: Powerdump + bypass uac + powerdump + minikatz*
[![ATTPwn: Powerdump + bypass uac + powerdump + minikatz](https://img.youtube.com/vi/VQHVgfgdJwM/0.jpg)](https://youtu.be/VQHVgfgdJwM)
### *ATTPwn: Generation of a basic threat plan and deployment on machine to check your controls/defenses)*
[![ATTPwn: Generation of a basic threat plan and deployment on machine to check your controls/defenses](https://img.youtube.com/vi/hyojkQHJxbA/0.jpg)](https://youtu.be/hyojkQHJxbA)



# License

This project is licensed under the GNU General Public License - see the LICENSE file for details

# Contact

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

This software doesn't have a QA Process. This software is a Proof of Concept.

If you have any problems, you can contact:

<pablo.gonzalezperez@telefonica.com> - *Ideas Locas CDCO - Telefónica*

<franciscojose.ramirezvicente@telefonica.com> - *Ideas Locas CDCO - Telefónica*

<victor.rodriguez.practicas@telefonica.com> - *Ideas Locas CDCO - Telefónica*

For more information please visit [https://www.elevenpaths.com](https://www.elevenpaths.com).
