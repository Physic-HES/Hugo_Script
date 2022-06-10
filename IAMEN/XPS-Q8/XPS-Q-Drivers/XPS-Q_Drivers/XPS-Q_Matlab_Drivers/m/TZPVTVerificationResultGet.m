function [errorCode, FileName, MinimumPosition, MaximumPosition, MaximumVelocity, MaximumAcceleration] = TZPVTVerificationResultGet(socketId, PositionerName)
%TZPVTVerificationResultGet :  TZ PVT trajectory verification result get
%
%	[errorCode, FileName, MinimumPosition, MaximumPosition, MaximumVelocity, MaximumAcceleration] = TZPVTVerificationResultGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		cstring FileName
%		doublePtr MinimumPosition
%		doublePtr MaximumPosition
%		doublePtr MaximumVelocity
%		doublePtr MaximumAcceleration


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
FileName = '';
for i = 1:103
	FileName = [FileName '          '];
end
MinimumPosition = 0;
MaximumPosition = 0;
MaximumVelocity = 0;
MaximumAcceleration = 0;

% lib call
[errorCode, PositionerName, FileName, MinimumPosition, MaximumPosition, MaximumVelocity, MaximumAcceleration] = calllib('XPS_C8_drivers', 'TZPVTVerificationResultGet', socketId, PositionerName, FileName, MinimumPosition, MaximumPosition, MaximumVelocity, MaximumAcceleration);
