function [errorCode, PCORawPositionX, PCORawPositionY, PCORawPositionZ] = XYZGroupPositionPCORawEncoderGet(socketId, GroupName, PositionX, PositionY, PositionZ)
%XYZGroupPositionPCORawEncoderGet :  Return PCO raw encoder positions
%
%	[errorCode, PCORawPositionX, PCORawPositionY, PCORawPositionZ] = XYZGroupPositionPCORawEncoderGet(socketId, GroupName, PositionX, PositionY, PositionZ)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		double PositionX
%		double PositionY
%		double PositionZ
%	* Output parameters :
%		int32 errorCode
%		doublePtr PCORawPositionX
%		doublePtr PCORawPositionY
%		doublePtr PCORawPositionZ


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
PCORawPositionX = 0;
PCORawPositionY = 0;
PCORawPositionZ = 0;

% lib call
[errorCode, GroupName, PCORawPositionX, PCORawPositionY, PCORawPositionZ] = calllib('XPS_Q8_drivers', 'XYZGroupPositionPCORawEncoderGet', socketId, GroupName, PositionX, PositionY, PositionZ, PCORawPositionX, PCORawPositionY, PCORawPositionZ);
