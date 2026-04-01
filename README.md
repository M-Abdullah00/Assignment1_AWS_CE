# 🎓 UniEvent – Deployment of a Scalable University Event Management System on AWS

---

## 📌 1. Introduction

With the increasing need for centralized platforms in universities, managing and accessing event information efficiently has become essential. This project presents **UniEvent**, a cloud-based web application designed to allow students to view university events and upload event-related media.

The system is deployed using Amazon Web Services (AWS) and follows modern cloud architecture principles. It is designed to be **scalable**, **secure**, and **fault-tolerant**, ensuring continuous availability even during peak usage periods such as student society drives or university festivals.

A key feature of this system is its ability to dynamically fetch event data from an external API, eliminating the need for manual data entry. All fetched data and uploaded media are securely stored in Amazon S3.

---

## 🏗️ 2. System Architecture Overview

```text
Internet → Application Load Balancer → EC2 Instances (Private Subnet) → S3 Storage
                                              ↓
                                        External API
```

---


---

# 🧱 PHASE 1 — AWS INFRASTRUCTURE SETUP

---

## 🔹 Virtual Private Cloud (VPC)

A custom VPC was created to isolate the network environment. The following components were configured:

* Public Subnets (for Load Balancer)
* Private Subnets (for EC2 instances)
* Internet Gateway attached
* Route tables configured for internet access

---

## 📷 Screenshot 1: VPC Configuration

<img width="844" height="569" alt="Screenshot 2026-03-28 213616" src="https://github.com/user-attachments/assets/7b888d1e-758f-488c-8ebc-8fa535895fe9" />

---

## 🔹 Security Groups

Security groups were configured to control traffic:

* Load Balancer: Allows HTTP (Port 80) from anywhere
* EC2 Instances: Allows HTTP only from Load Balancer
  
<img width="1061" height="646" alt="Screenshot 2026-03-28 220409" src="https://github.com/user-attachments/assets/44f8b240-447d-4c44-bf56-6ae3344d39d0" />

<img width="1086" height="627" alt="Screenshot 2026-03-28 222304" src="https://github.com/user-attachments/assets/2c23e08b-af1d-4676-b367-37dcaf7b5625" />


---

# 🧱 PHASE 2 — COMPUTE AND ACCESS MANAGEMENT

---

## 🔹 EC2 Instances

* Two EC2 instances were launched in the private subnet
* Instances host the UniEvent application
* Accessed securely using Session Manager (no SSH)

---

## 📷 Screenshot 3: EC2 Instances

<img width="1568" height="299" alt="Screenshot 2026-04-01 201331" src="https://github.com/user-attachments/assets/0bf6b72e-c7c1-42ff-ba75-d60a095cb273" />

---

## 🔹 IAM Role Configuration

An IAM Role was attached to EC2 instances with permissions:

* AmazonS3FullAccess
* AmazonSSMManagedInstanceCore

This ensures secure and credential-free access to AWS services.

---

## 📷 Screenshot 4: IAM Role

<img width="1112" height="391" alt="Screenshot 2026-03-28 223408" src="https://github.com/user-attachments/assets/92148295-02c0-48ae-be1d-5fb4069fc17f" />

---

# 🧱 PHASE 3 — STORAGE AND LOAD BALANCING

---

## 🔹 Amazon S3

Bucket used:

```
unievent-images-12345
```

Used to store:

* Event data (`events.json`)
* Uploaded images

---

## 📷 Screenshot 5: S3 Bucket

<img width="1020" height="407" alt="Screenshot 2026-04-01 201707" src="https://github.com/user-attachments/assets/13ee260d-9154-4c52-9fbd-a4d9147b3868" />

---

## 🔹 Application Load Balancer (ALB)

* Distributes incoming traffic across EC2 instances
* Ensures high availability
* Performs health checks

---

## 📷 Screenshot 6: Load Balancer

<img width="826" height="415" alt="Screenshot 2026-03-28 230020" src="https://github.com/user-attachments/assets/d3523e23-d7eb-4ac3-8be2-e411ac211d86" />

---

# 🧱 PHASE 4 — APPLICATION DEPLOYMENT

---

## 🔹 Application Setup

The application was developed using Python Flask and deployed on EC2.

### Installation Steps:

```bash
yum update -y
yum install python3 -y
yum install python3-pip -y
pip3 install flask requests boto3
```
<img width="1084" height="293" alt="Screenshot 2026-03-28 232604" src="https://github.com/user-attachments/assets/d774029a-c7e7-4e77-8263-6b69d31489c5" />

---

## 🔹 Application Functionality

* Fetches event data from external API
* Stores fetched data in S3
* Displays events on web page
* Allows image upload to S3

---

## 🔹 Running the Application

```bash
sudo python3 app.py
```

---

## 📷 Screenshot 7: Application Running

<img width="796" height="577" alt="Screenshot 2026-03-31 024410" src="https://github.com/user-attachments/assets/a9133381-1548-49ff-aa10-1e077114e053" />

---

# 🧱 PHASE 5 — API INTEGRATION

---

## 🔹 External API Used

```
https://jsonplaceholder.typicode.com/posts
```

This API provides structured JSON data used as event information.

---

## 📷 Screenshot 8: Website Output

<img width="1894" height="991" alt="Screenshot 2026-03-31 023752" src="https://github.com/user-attachments/assets/162f2b7d-7343-4532-aa22-960c42997a10" />

---

# 🧱 PHASE 6 — DATA STORAGE VERIFICATION

---

* On accessing the application, event data is stored in S3 as `events.json`
* Uploaded images are also stored in the same bucket

---

## 📷 Screenshot 9: S3 Stored Data

<img width="1488" height="739" alt="Screenshot 2026-03-31 024236" src="https://github.com/user-attachments/assets/d35a489b-5b03-4e12-a39f-0924f422f1ac" />


---

# 🧱 PHASE 7 — TESTING AND VALIDATION

---

## 🔹 API Functionality Test

* Verified that event data is fetched and stored in S3

## 🔹 Upload Functionality Test

* Verified successful image upload to S3

---

## 📷 Screenshot 10: Image Upload 

<img width="545" height="336" alt="Screenshot 2026-03-31 023836" src="https://github.com/user-attachments/assets/b037d6bc-2af3-4421-a02f-f14d266956ee" />
<img width="501" height="225" alt="Screenshot 2026-03-31 024120" src="https://github.com/user-attachments/assets/a1f66360-46db-4f11-886e-86766cf5c2e2" />

---

# 🧱 PHASE 8 — SECURITY IMPLEMENTATION

---

* EC2 instances are placed in private subnet
* No direct internet access to instances
* Access controlled via Load Balancer
* IAM roles used instead of hardcoded credentials
* Security groups restrict traffic flow

---

# 🧱 PHASE 9 — SCALABILITY AND AVAILABILITY

---

* Multiple EC2 instances deployed
* Load Balancer distributes incoming traffic
* System remains operational even if one instance fails

<img width="1872" height="294" alt="Screenshot 2026-03-31 022002" src="https://github.com/user-attachments/assets/3b0c421a-bbed-457e-840b-a97303eedff7" />

---

# 🏁 10. Conclusion

The UniEvent system successfully demonstrates a scalable, secure, and fault-tolerant cloud application using AWS services. The architecture ensures high availability while dynamically fetching and storing data. This project effectively highlights the practical application of cloud computing concepts in real-world scenarios.


---

