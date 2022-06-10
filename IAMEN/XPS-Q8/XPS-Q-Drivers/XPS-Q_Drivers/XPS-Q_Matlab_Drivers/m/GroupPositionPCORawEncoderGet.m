function [errorCode, PCORawPositionX, PCORawPositionY] = GroupPositionPCORawEncoderGet(socketId, GroupName, PositionX, PositionY)
%GroupPositionPCORawEncoderGet :  Return PCO raw encoder positions
%
%	[errorCode, PCORawPositionX, PCORawPositionY] = GroupPositionPCORawEncoderGet(socketId, GroupName, PositionX, PositionY)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		double PositionX
%		double PositionY
%	* Output parameters :
%		int32 errorCode
%		doublePtr PCORawPositionX
%		doublePtr PCORawPositionY


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
PCORawPositionX = 0;
PCORawPositionY = 0;

% lib call
[errorCode, GroupName, PCORawPositionX, PCORawPositionY] = calllib('XPS_Q8_drivers', 'GroupPositionPCORawEncoderGet', socketId, GroupName, PositionX, PositionY, PCORawPositionX, PCORawPositionY);
