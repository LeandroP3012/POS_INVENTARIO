class User {
  final int id;
  final String username;
  final String fullName;
  final String userType;
  final int? roleId;
  final String accessToken;

  User({
    required this.id,
    required this.username,
    required this.fullName,
    required this.userType,
    this.roleId,
    required this.accessToken,
  });

  factory User.fromJson(Map<String, dynamic> json) => User(
        id: json['user_id'],
        username: json['username'],
        fullName: json['full_name'],
        userType: json['user_type'],
        roleId: json['role_id'],
        accessToken: json['access_token'],
      );

  bool get isAdmin => userType == 'admin';
  bool get isManager => userType == 'manager' || userType == 'supervisor';
}
